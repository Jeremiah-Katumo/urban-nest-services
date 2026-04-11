


class TicketService:

    def categorize_issue(self, query: str):
        query = query.lower()

        if any(query for k in ["payment", "rent"]):
            return "PAYMENT"
        if any(query for k in ["booking", "reservation"]):
            return "BOOKING"
        if any(query for k in ["repair", "broken"]):
            return "MAINTENANCE"
        return "OTHER"

    def should_create_ticket(self, ai_response: str):
        failure_keywords = ["don't understand", "cannot help", "unknown"]
        return any(k in ai_response.lower() for k in failure_keywords)