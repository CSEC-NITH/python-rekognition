import boto3, os, json, math, sys
from pathlib import Path


client = boto3.client('rekognition')

FILE_NAME = raw_input("Enter file name: ")

# check if file exists
if not Path(FILE_NAME).is_file():
    print("Could not find file.")
    exit()

## check file size
if os.path.getsize(FILE_NAME) > 5242880:
    print("File too large.")
    exit()

print("Choose Task: ")
print("1. Text detection")
print("2. Facial analysis")
print("3. Scene detection")
print("Other: exit")
choice = input("Enter choice number: ")

with open(FILE_NAME, "rb") as imageFile:
  f = imageFile.read()
  b = bytearray(f)

# Facial analysis
if choice == 2:

    response = client.detect_faces(
        Image={
            'Bytes': f
        },
        Attributes=[
            'ALL'
        ]
    )

    print("Detected " + str(len(response["FaceDetails"])) + " face(s).")
    i = 1

    for face in response["FaceDetails"]:
        print("Face " + str(i) + ": ")
        print("Age Range: " + str(face["AgeRange"]["Low"]) + " to " + str(face["AgeRange"]["High"]))
        print("Emotions: "),

        for emotion in face["Emotions"]:
            print(emotion["Type"] + "(" + str(math.floor(emotion["Confidence"])) + "%) "),

        print("\nGender: " + face["Gender"]["Value"] + "(" + str(math.ceil(face["Gender"]["Confidence"])) + "% Confidence)")
        print("Facial Hair: Beard - " + str(face["Beard"]["Value"]) + "(" + str(math.ceil(face["Beard"]["Confidence"])) + ") Mustache - " + str(face["Mustache"]["Value"]) + "(" + str(math.ceil(face["Mustache"]["Confidence"])) + ")")
        print("Smile: " + str(face["Smile"]["Value"]) + "(" + str(math.ceil(face["Smile"]["Confidence"])) + "% Confidence)")

        print("==================================")
        i += 1

# Scene Detection
elif choice == 3:
    response = client.detect_labels(
        Image={
            'Bytes': f
        },
        MinConfidence=50
    )
    print("The following labels were detected in the image: ")
    for item in response["Labels"]:
        print(item["Name"] + ": " + str(item["Confidence"]))

# Text Detection
elif choice == 1:
    response = client.detect_text(
        Image={
            'Bytes': f
        }
    )

    for text in response["TextDetections"]:
        print(text["DetectedText"])

else:
    exit()

if('-v' in sys.argv):
    print json.dumps(response, indent=4, sort_keys=True)
