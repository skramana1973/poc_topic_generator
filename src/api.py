from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from pathlib import Path
from src.poc_topic_generator.crew import PocTopicGeneratorCrew
import uuid
# Define a request model to validate input
class TopicRequest(BaseModel):
    topic: str

# Initialize FastAPI app
app = FastAPI()

# Initialize your Crew class

crew_instance = PocTopicGeneratorCrew()

@app.post("/generate")
async def generate_topic_report(request: TopicRequest):
    """
    API endpoint to trigger the PocTopicGeneratorCrew to process the topic.
    
    Args:
        request (TopicRequest): The topic for the crew to process.

    Returns:
        JSON: Result of the crew's task execution.
    """
    try:
        # Prepare input for the crew
        inputs = {'topic': request.topic}

        # Run the crew's tasks
        result = crew_instance.crew().kickoff(inputs=inputs)
        print(f"Crew AI Response : {result.raw}")
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")


@app.post("/report")
async def generate_topic_report_file(request: TopicRequest):
    try:
        # Generate a unique filename for each report
        unique_filename = f"report_{uuid.uuid4().hex}.md"
        
        # Prepare inputs for the crew
        inputs = {
        'topic': request.topic
        
        }
       
        # Run the crew's tasks with the unique filename
        result = crew_instance.crew().kickoff(inputs=inputs)
        #print(f"Crew AI Response : {response.result.raw}")
       
        # Get the path to the generated file
        current_dir = Path(__file__).resolve().parent
        output_file_path = current_dir.parent / unique_filename
        with open(output_file_path, 'w') as file:
            file.write(result.raw)
        # Check if the file exists
        if not output_file_path.exists():
            raise HTTPException(status_code=500, detail="File not found after generation.")

        # Return the file as a response
        return FileResponse(
            path=str(output_file_path),
            filename=unique_filename,
            media_type='application/octet-stream',
            headers={"Content-Disposition": f"attachment; filename={unique_filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")
