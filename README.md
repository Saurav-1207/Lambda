
# AWS Lambda Audio Transcription Service

This AWS Lambda function transcribes audio files using the Groq API. It accepts base64-encoded audio files sent via API Gateway, transcribes the audio, and returns the transcription as a JSON response.

## Requirements

- AWS account with Lambda and API Gateway permissions
- Groq API key (stored as an environment variable in Lambda)
- Audio file to test with (in WAV format)

## Setup and Deployment

### 1. Configure Environment Variables
1. In the AWS Lambda Console, set the environment variable for the Groq API key.
    - Go to your Lambda function and select **Configuration** > **Environment Variables**.
    - Add a variable:
      - **Key**: `GROQ_API_KEY`
      - **Value**: `<Your_Groq_API_Key>`

### 2. Deploy Lambda Function
1. Copy the code from `lambda_function.py` into the Lambda function editor in AWS Lambda.
2. Make sure your Lambda function has permissions to write to `/tmp` and to connect to the Groq API.

### 3. Configure API Gateway
1. Create an API Gateway and set up a POST method for your Lambda function.
2. Deploy the API and note the URL generated (in this case, `https://bbh4o05euh.execute-api.us-east-1.amazonaws.com/dev/transcribe`).

## Testing the API with `curl`

### Sending Audio File via `curl`

To test the Lambda function with an audio file, you can use the following `curl` command, which sends a WAV file to the API endpoint:

```bash
curl -X POST "https://bbh4o05euh.execute-api.us-east-1.amazonaws.com/dev/transcribe"      -H "Content-Type: audio/wav"      --data-binary "@C:/New/Path/To/live_recording.wav"
```

- **Note**: Replace `C:/New/Path/To/live_recording.wav` with the path to your audio file.

### Response

The response from the API should be in JSON format, containing the transcription. An example response might look like this:

```json
{
  "transcription": "This is the transcribed text."
}
```

## Troubleshooting

- **400 Bad Request**: Ensure the file path and format are correct. The audio file must be in WAV format.
- **500 Internal Server Error**: Check if the Groq API key is correctly set in Lambda and verify Lambda permissions.

### Debugging Tips
- Use `print` statements in the Lambda function to log request details and debug errors.
- Check Lambda logs in **CloudWatch Logs** for detailed error messages.

