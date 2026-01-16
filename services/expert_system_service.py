"""Expert System Service - business logic for disease diagnosis"""

class ExpertSystem:
    """Expert system for diagnosing rice diseases based on symptoms"""
    
    def __init__(self, db_session, Disease, Symptom, DiseaseSymptom, ExpertRule):
        self.db = db_session
        self.Disease = Disease
        self.Symptom = Symptom
        self.DiseaseSymptom = DiseaseSymptom
        self.ExpertRule = ExpertRule
    
    def has_symptom(self, symptom_name, selected_symptom_ids):
        """Check if a symptom is in the selected symptoms"""
        symptom = self.Symptom.query.filter_by(name=symptom_name).first()
        if symptom:
            return symptom.id in selected_symptom_ids
        return False
    
    def evaluate_rule(self, rule, selected_symptom_ids):
        """Evaluate an expert rule condition"""
        try:
            # Create a safe evaluation context
            context = {
                'has_symptom': lambda name: self.has_symptom(name, selected_symptom_ids),
                'True': True,
                'False': False,
                'and': lambda x, y: x and y,
                'or': lambda x, y: x or y,
                'not': lambda x: not x
            }
            
            # Evaluate the condition
            result = eval(rule.condition, {"__builtins__": {}}, context)
            return result
        except:
            return False
    
    def diagnose(self, selected_symptom_ids):
        """
        Diagnose diseases based on selected symptoms
        
        Args:
            selected_symptom_ids: List of symptom IDs selected by user
            
        Returns:
            List of dictionaries with disease information and confidence scores
        """
        if not selected_symptom_ids:
            return []
        
        results = []
        
        # Method 1: Rule-based diagnosis
        rules = self.ExpertRule.query.all()
        rule_matches = {}
        
        for rule in rules:
            if self.evaluate_rule(rule, selected_symptom_ids):
                disease = self.Disease.query.get(rule.disease_id)
                if disease:
                    if disease.id not in rule_matches:
                        rule_matches[disease.id] = {
                            'disease': disease,
                            'confidence': rule.confidence,
                            'method': 'rule-based'
                        }
                    else:
                        # If multiple rules match, take the highest confidence
                        rule_matches[disease.id]['confidence'] = max(
                            rule_matches[disease.id]['confidence'],
                            rule.confidence
                        )
        
        # Method 2: Symptom matching (calculate similarity)
        diseases = self.Disease.query.all()
        symptom_matches = {}
        
        for disease in diseases:
            # Get all symptoms for this disease
            disease_symptoms = self.DiseaseSymptom.query.filter_by(disease_id=disease.id).all()
            disease_symptom_ids = [ds.symptom_id for ds in disease_symptoms]
            
            if not disease_symptom_ids:
                continue
            
            # Calculate match ratio
            matched_symptoms = set(selected_symptom_ids) & set(disease_symptom_ids)
            match_ratio = len(matched_symptoms) / len(disease_symptom_ids)
            
            # Calculate confidence based on match ratio
            # Higher match ratio = higher confidence
            confidence = min(match_ratio * 1.2, 1.0)  # Cap at 1.0
            
            if confidence > 0.3:  # Only include if confidence > 30%
                if disease.id not in symptom_matches:
                    symptom_matches[disease.id] = {
                        'disease': disease,
                        'confidence': confidence,
                        'method': 'symptom-matching',
                        'matched_symptoms_count': len(matched_symptoms),
                        'total_symptoms_count': len(disease_symptom_ids)
                    }
        
        # Combine results, prioritizing rule-based matches
        all_matches = {}
        
        # Add rule-based matches (higher priority)
        for disease_id, match_info in rule_matches.items():
            all_matches[disease_id] = match_info
        
        # Add symptom-based matches (if not already in rule-based)
        for disease_id, match_info in symptom_matches.items():
            if disease_id not in all_matches:
                all_matches[disease_id] = match_info
            else:
                # If both methods match, combine confidence (weighted average)
                rule_conf = all_matches[disease_id]['confidence']
                symptom_conf = match_info['confidence']
                # Rule-based gets 70% weight, symptom-based gets 30%
                combined_conf = (rule_conf * 0.7) + (symptom_conf * 0.3)
                all_matches[disease_id]['confidence'] = min(combined_conf, 1.0)
                all_matches[disease_id]['method'] = 'combined'
        
        # Convert to list and sort by confidence (descending)
        results = list(all_matches.values())
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        return results
