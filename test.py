from src.ats_insight_agent.parser.docling_parser import DoclingParser
from src.ats_insight_agent.nodes.resume_processor_node import ResumeProcessor
from src.ats_insight_agent.utils.Utility import Utility

if __name__ == "__main__":
    resume_processor = ResumeProcessor(None)
    resume_processor.process_resume_file("/Users/murtuzasaifee/Documents/Personal/Codes/AgenticAIWorkspace/ATS-Insight-Agent/test_resume.pdf")