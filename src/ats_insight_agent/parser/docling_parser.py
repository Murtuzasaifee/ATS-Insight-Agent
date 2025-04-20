from loguru import logger
import hashlib
from typing import Any, Dict
import json
from docling.document_converter import DocumentConverter
from src.ats_insight_agent.dto.resume_document import ResumeDocument
from pathlib import Path
from docling_core.types import DoclingDocument


class DoclingParser:
    def __init__(self, supported_extensions):
        self.supported_extensions = supported_extensions
        pass
    
    
    def generate_document_id(self, file_path: str, content: str) -> str:
        """Generate a unique ID for a document based on its path and content."""
        unique_string = f"{file_path}:{content[:1000]}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    
    def extract_metadata(self, doc: DoclingDocument) -> Dict[str, Any]:
        """Extract metadata from a parsed DoclingDocument."""
        metadata: Dict[str, Any] = {}

        try:
            # dump to a dict
            doc_dict = doc.export_to_dict()
            
            logger.debug(f"Docling Document: {json.dumps(doc_dict)}")

            origin = doc_dict.get("origin", {})
            metadata["original_filename"] = origin.get("filename")
            metadata["mimetype"]          = origin.get("mimetype")
            metadata["uri"]               = origin.get("uri")
            metadata["binary_hash"]       = origin.get("binaryHash")

            if doc_dict.get("name"):
                metadata["title"] = doc_dict["name"]
            if doc_dict.get("version"):
                metadata["version"] = doc_dict["version"]
        
            try:
                metadata["num_pages"] = doc.num_pages()
            except:
                metadata["num_pages"] = len(doc_dict.get("pages", []))

            has_education = False
            has_experience = False
            has_skills = False

            for text_item in doc_dict.get("texts", []):
                label = text_item.get("label").lower()
                if label in ("section_header", "title"):
                    heading_text = text_item.get("text", "").lower()
                    logger.debug(f"heading_text: {heading_text}")
                    if any(k in heading_text for k in ["education", "academic", "degree"]):
                        has_education = True
                    if any(k in heading_text for k in ["experience", "work", "employment", "career"]):
                        has_experience = True
                    if any(k in heading_text for k in ["skill", "expertise", "qualification", "proficiency","technology"]):
                        has_skills = True

            metadata["has_education"]   = has_education
            metadata["has_experience"]  = has_experience
            metadata["has_skills"]      = has_skills

        except Exception as e:
            logger.warning(f"Error extracting metadata: {e}")

        return metadata
    
    def parse_resume(self, file_path: str) -> ResumeDocument:
        """
        Parse a resume file and extract its content and metadata.
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            ResumeDocument object containing parsed information
        """
        file_path = Path(file_path).resolve()
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check if file extension is supported
        if file_path.suffix.lower() not in self.supported_extensions:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        try:
            # Parse document using docling
            logger.info(f"Parsing document: {file_path}")
            converter = DocumentConverter()
            result = converter.convert(str(file_path))
            doc = result.document
            
            # Extract content and metadata
            content = doc.export_to_text()
            metadata = self.extract_metadata(doc)
            
            # Create resume document
            doc_id = self.generate_document_id(str(file_path), content)
            resume_doc = ResumeDocument(
                doc_id=doc_id,
                filename=file_path.name,
                file_path=str(file_path),
                content=content,
                metadata=metadata
            )
            
            logger.info(f"Successfully parsed document: {file_path.name} (ID: {doc_id})")
            return resume_doc
            
        except Exception as e:
            logger.error(f"Failed to parse document {file_path}: {str(e)}")
            raise