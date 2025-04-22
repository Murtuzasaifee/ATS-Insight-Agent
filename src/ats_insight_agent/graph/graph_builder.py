from langgraph.graph import StateGraph,START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables.graph import MermaidDrawMethod
from src.ats_insight_agent.state.ats_state import ATSState
from src.ats_insight_agent.nodes.resume_processor_node import ResumeProcessor
from src.ats_insight_agent.dto.config import Config
from src.ats_insight_agent.vectorstore.milvus_store import MilvusStore
    
class GraphBuilder:
    
    def __init__(self):
        self.graph_builder = StateGraph(ATSState)
        self.memory = MemorySaver()
                
    
    def set_groq_llm(self, groq_llm):
        self.groq_llm = groq_llm
    
    
    def set_gemini_llm(self, gemini_llm):
        self.gemini_llm = gemini_llm
        
        
    def set_openai_llm(self, openai_llm):
        self.openai_llm = openai_llm
    
    
    def build_sdlc_graph(self, milvus_store: MilvusStore):
        """
            Configure the graph by adding nodes, edges
        """
        
        self.resume_processor = ResumeProcessor(self.groq_llm, milvus_store,config=Config())
        
        self.graph_builder.add_node("process_resume", self.resume_processor.process_resume_file)
        
        self.graph_builder.add_edge(START, "process_resume")
        self.graph_builder.add_edge("process_resume", END)    
         
        
    def setup_graph(self, milvus_store: MilvusStore):
        """
        Sets up the graph
        """
        self.build_sdlc_graph(milvus_store)
        return self.graph_builder.compile(
            interrupt_before=[],checkpointer=self.memory
        )
        
             
    # def setup_graph(self):
    #     """
    #     Sets up the graph
    #     """
    #     self.build_sdlc_graph()
    #     graph =self.graph_builder.compile(
    #         interrupt_before=[
    #             'get_user_requirements',
    #             'review_user_stories',
    #             'review_design_documents',
    #             'code_review',
    #             'security_review',
    #             'review_test_cases',
    #             'qa_review'
    #         ],checkpointer=self.memory
    #     )
    #     self.save_graph_image(graph)         
    #     return graph
    
    
    def save_graph_image(self,graph):
        # Generate the PNG image
        img_data = graph.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API
            )

        # Save the image to a file
        graph_path = "workflow_graph.png"
        with open(graph_path, "wb") as f:
            f.write(img_data)        
            
        