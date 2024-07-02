from models import Metadata, Document, ResponseBody

def get_mock_data_response(query) -> ResponseBody:
    return ResponseBody(
        question=query,
        results_summary="The author of the article is Hamel.",
        documents=[
            Document(
                page_content=[
                    "[...] mandates the testing and maintenance of protection system components to ensure the reliability [...]",
                    "[...] additional content here to showcase multiple pages or sections [...]" 
                ],
                metadata=Metadata(
                    source_url="https://example.com/docs/mandate",
                    id="be78adbd-d0b8-40bf-966a-71c828cf6cfe",
                    collection_name="Websites"
                ),
                type="Document"
            ),
            Document(
                page_content=[
                    "[...] mandates the testing and maintenance of protection system components to ensure the reliability [...]",
                    "[...] additional content here to showcase multiple pages or sections [...]"  
                ],
                metadata=Metadata(
                    source_url="https://example.com/docs/relays",
                    id="0fbf802ae-99fb-4f62-93ee-721831117b3c",
                    collection_name="Websites"
                ),
                type="Document"
            )
        ]
    )
