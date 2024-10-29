import json
import os
import base64
from groq import Groq

# Initialize the Groq client with the API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def lambda_handler(event, context):
    try:
        # Debug logging
        print("Event:", json.dumps(event))

        # Check if the body is base64 encoded (API Gateway setting)
        is_base64_encoded = event.get('isBase64Encoded', False)
        
        if is_base64_encoded:
            audio_data = base64.b64decode(event['body'])  # Decode base64
        else:
            audio_data = event['body'].encode('utf-8') if isinstance(event['body'], str) else event['body']
        
        # Save the audio data to a temporary file
        download_path = '/tmp/live_recording.wav'
        with open(download_path, 'wb') as file:
            file.write(audio_data)

        # Transcribe the audio
        with open(download_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=("live_recording.wav", audio_file, "audio/wav"),
                model="whisper-large-v3-turbo",
                language="en",
                response_format="json"
            )
            print("Transcription successful")
        
        # Get the transcribed text
        transcribed_text = transcription.text
        print("Transcribed Text:", transcribed_text)

        # Clean up
        os.remove(download_path)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST'
            },
            'body': json.dumps({
                'transcription': transcribed_text
            })
        }

    except Exception as e:
        print(f"Error details: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': f'An error occurred: {str(e)}'})
        }
