# Report generator
class ReportGenerator:
    def __init__(self, extractor: LogExtractor, openai_client: OpenAIClient):
        self.extractor = extractor
        self.openai_client = openai_client

    def generate_report(self):
        logs = self.extractor.extract_logs()
        errors = self.extractor.filter_errors()
        summary = self.openai_client.summarize(errors)
        return f"Report:\nLogs: {logs}\nErrors: {errors}\nSummary: {summary}"

# Example usage
if __name__ == "__main__":
    # Instantiate the OpenAI client with an API key
    openai_client = OpenAIClient(api_key='your-openai-api-key')