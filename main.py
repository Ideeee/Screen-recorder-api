from pprint import pprint
from uuid import uuid4
from fastapi import APIRouter, FastAPI, HTTPException, UploadFile
# from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.exceptions import ResourceNotFoundError 
from typing import List
import uvicorn, base64

from schemas import VideoData

app = FastAPI()

@app.get('/')
async def root():
    return{'message': 'Na who give up, mess up'}

connect_str = "DefaultEndpointsProtocol=https;AccountName=chromextension;AccountKey=Kevp1GcMr3Rc8JfWRBWXXf9mV1sMEThEP9soX++nWtoePisftZWJVitEKaklwXaajhPFb3XrTcDH+AStTpPU9Q==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "test"
container_client = blob_service_client.get_container_client(container_name)




@app.post("/api/start-recording", status_code=201)
async def create_video_file(file_type: str = 'video/mp4'):
    """
    This endpoint creates a new empty video file in the blob storage and returns the id of the created file.\n
    It takes in an optional file type parameter which defaults to mp4
    """
    type = file_type
    id = uuid4().hex

    try:
        blob_client = container_client.get_blob_client(id)

        blob_client.create_append_blob()

        # Get the existing blob properties
        properties = blob_client.get_blob_properties()

        # Set the content_type and content_language headers, and populate the remaining headers from the existing properties
        blob_headers = ContentSettings(content_type=type,
                                      content_encoding=properties.content_settings.content_encoding,
                                      content_language="en-US",
                                      )
        
        blob_client.set_http_headers(blob_headers)

    except Exception as e:
        print(e)
        raise HTTPException(401, "Could not create file")
    
    return { "message": "Video file created successfully",
            "file_id": id 
            }

@app.post("/api/collect-video-data", status_code = 201)
async def collect_video_data(data: VideoData):
     """
     This endpoint collects the video data in chunks(blobs) from the extension and appends it to the empty video file in the blob storage.\n
     It takes in a VideoData object which contains the blob and the id of the file to be appended to.\n

     """

     blob = base64.b64decode(data.blob)


     try:
        print('here')
        blob_client = container_client.get_blob_client(data.id)

        blob_client.append_block(blob, length=len(blob))

     except ResourceNotFoundError as e:
        print(e)
        raise HTTPException(status_code=404, detail=f"Blob '{id}' not found")

     except Exception as e:
         print(e)
         raise HTTPException(401, "Could not write to file")
      
     return {"message" : "Successful",
             "file_id": data.id
             }
     

@app.post("/api/finalise-video", status_code = 200)
async def finalise_video(file_id: str):
    """
    Returns the url that can be used to stream the video file
    """
    
    try:
        blob_client = container_client.get_blob_client(file_id)
        url = blob_client.url

        # properties = blob_client.get_blob_properties()
        # pprint(properties)

    except Exception as e:
        print(e)
        return HTTPException(401, "Something went wrong..")
    
    return {
            'message':'Video recording successful',
            'url': url,
            'file_id': file_id
           }



    # with open(f"videos/{video_id}", 'wb'):
    #     pass


    # with open(f"videos/{id}", "ab") as file:
        # file.write(blob)

    # with open(f"videos/{file_id}", 'rb') as file:
        # f = await file.read()
        # await blob_client.upload_blob(f)


# async def createcontainer(id: str):
    
#      async with blob_service_client:
#             try:
#                 container_client = await blob_service_client.create_container(name=id, public_access='container')
#             except Exception as e:
#                  print(e)
#                  return HTTPException(401, "Sorry, something went wrong....")
     
#      return {"file_id" : id}
     
     


if __name__ == "__main__":
    uvicorn.run(app='main:app', port=7000, reload=True)