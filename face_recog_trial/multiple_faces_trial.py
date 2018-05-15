from PIL import Image, ImageDraw
import face_recognition

print("Loading known face image(s)")

josh_image = face_recognition.load_image_file("josh.jpg")
mahesh_image = face_recognition.load_image_file("mahesh.jpg")
dan_image = face_recognition.load_image_file("dan.jpg")
joe_image = face_recognition.load_image_file("joe.jpg")
bonnie_image = face_recognition.load_image_file("bonnie.jpg")
eric_image = face_recognition.load_image_file("eric.jpg")
jenna_image = face_recognition.load_image_file("jenna.jpg")

print("Encoding images")
josh_face_encoding = face_recognition.face_encodings(josh_image)[0]
mahesh_face_encoding = face_recognition.face_encodings(mahesh_image)[0]
dan_face_encoding = face_recognition.face_encodings(dan_image)[0]
joe_face_encoding = face_recognition.face_encodings(joe_image)[0]
bonnie_face_encoding = face_recognition.face_encodings(bonnie_image)[0]
eric_face_encoding = face_recognition.face_encodings(eric_image)[0]
jenna_face_encoding = face_recognition.face_encodings(jenna_image)[0]

known_face_encodings = [
josh_face_encoding,
mahesh_face_encoding,
dan_face_encoding,
joe_face_encoding,
bonnie_face_encoding,
eric_face_encoding,
jenna_face_encoding
]

known_face_names = [
    "Josh",
    "Mahesh",
    "Dan",
    "Joe",
    "Bonnie",
    "Eric",
    "Jenna"
]

unknown_image = face_recognition.load_image_file("unknown3.jpg")

print("Finding face locations")
face_locations = face_recognition.face_locations(unknown_image)
face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

pil_image = Image.fromarray(unknown_image)
# Create a Pillow ImageDraw Draw instance to draw with
draw = ImageDraw.Draw(pil_image)

for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    name = "Unknown"

    # If a match was found in known_face_encodings, just use the first one.
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    # Draw a box around the face using the Pillow module
    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

    # Draw a label with a name below the face
    text_width, text_height = draw.textsize(name)
    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
    draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))


# Remove the drawing library from memory as per the Pillow docs
del draw

# Display the resulting image
pil_image.show()
