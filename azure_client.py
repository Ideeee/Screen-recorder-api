from azure.storage.blob import BlobServiceClient, ContentSettings
import whisper

model = whisper.load_model('base')
option = whisper.DecodingOptions(fp16=False)

connect_str = "DefaultEndpointsProtocol=https;AccountName=chromextension;AccountKey=Kevp1GcMr3Rc8JfWRBWXXf9mV1sMEThEP9soX++nWtoePisftZWJVitEKaklwXaajhPFb3XrTcDH+AStTpPU9Q==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "test"
container_client = blob_service_client.get_container_client(container_name)
