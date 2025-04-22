from pymilvus import connections, utility
import re    
import html

class Utility:
    
    def __init__(self):
        pass
    
    def drop_milvus_collection(self, connections, collection_name):
        connections.connect(
            alias="default",
            host="127.0.0.1",
            port="19530"
        )
         
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
            print(f"Dropped Milvus collection: {collection_name}")
        else:
            print(f"No collection named '{collection_name}' found.")
            


    def clean_resume_text(self, text: str) -> str:
        """
        Clean resume content by removing markdown, html entities, tables, and normalizing whitespace.

        Args:
            text (str): Raw extracted resume content.

        Returns:
            str: Cleaned resume text.
        """

        # 1. Decode HTML entities (e.g., &amp; -> &)
        text = html.unescape(text)

        # 2. Remove markdown headers and bullets
        text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)  # ## headers
        text = re.sub(r"-\s*●?", "", text)                          # Bullets like - or - ●

        # 3. Remove Markdown table formatting
        text = re.sub(r"\|[-\s|]+\|", "", text)  # Table dividers
        text = re.sub(r"\|", " ", text)          # Remaining table pipes

        # 4. Normalize excessive newlines and spaces
        text = re.sub(r"\n{2,}", "\n", text)       # Multiple newlines -> single
        text = re.sub(r"[ \t]{2,}", " ", text)     # Multiple spaces/tabs -> single
        text = re.sub(r"\s{2,}", " ", text)        # Any excessive space

        # 5. Strip leading/trailing whitespace
        text = text.strip()

        return text
    
    