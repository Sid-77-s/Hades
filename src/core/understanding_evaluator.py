from src.models.mission import MissionUnderstanding, InformationSource, Criticality

class UnderstandingEvaluator:
    @staticmethod
    def evaluate(understanding: MissionUnderstanding) -> bool:
        """
        Evaluates whether the mission understanding is sufficient to reach Mission Lock.
        Returns True if locked, False otherwise.
        """
        # 1. Check for contradictions
        if len(understanding.contradictions) > 0:
            return False
            
        # 2. Check for missing CRITICAL information
        fields_to_check = [
            understanding.objective,
            understanding.desired_outcome,
            understanding.success_criteria,
            understanding.context,
            understanding.constraints,
            understanding.priorities,
            understanding.preferences,
            understanding.important_decisions
        ]
        
        for field in fields_to_check:
            if field.criticality == Criticality.CRITICAL:
                # If a critical field is completely unknown, we cannot lock.
                if field.source == InformationSource.UNKNOWN or not field.value:
                    return False
        
        # 3. Check for User Alignment
        # The mutual_understanding_reached flag must be explicitly set to True
        # by the ConversationalDecision system when the user confirms alignment.
        if not understanding.mutual_understanding_reached:
            return False
            
        return True
