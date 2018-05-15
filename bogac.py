from PIL import Image, ImageDraw
import face_recognition
import os
import numpy as np

def data_prep():
	main_path = os.getcwd()
	path_to_known_people = main_path + "/known_people1"

	os.chdir(path_to_known_people)

	folder = os.listdir(path_to_known_people)

	known_names = []
	known_images = []
	known_image_encodings = []


	print("Loading Images")
	for file in folder:

		if file.startswith("."):
			continue

		#load the image
		new_image = face_recognition.load_image_file(file)
		known_images.append(new_image)

		#get the name
		name = os.path.splitext(file)[0]
		known_names.append(name)

	print("Encoding Images")
	for image in known_images:

		new_enconding = face_recognition.face_encodings(image)[0]
		known_image_encodings.append(new_enconding)

	os.chdir(main_path)
	return known_images, known_names, known_image_encodings

def unknown_image_prep():
	print("Getting unknown image")
	unknown_image = face_recognition.load_image_file("images/latest.jpg")
	face_locations = face_recognition.face_locations(unknown_image)
	face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

	return unknown_image, face_locations, face_encodings

def draw_image(unknown_image, face_locations, face_encodings, known_image_encodings, known_names):
	print("Drawing image")
	pil_image = Image.fromarray(unknown_image)
	# Create a Pillow ImageDraw Draw instance to draw with
	draw = ImageDraw.Draw(pil_image)

	names = []

	for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
	    # See if the face is a match for the known face(s)
	    matches = face_recognition.compare_faces(known_image_encodings, face_encoding)

	    name = "Unknown"

	    # If a match was found in known_face_encodings, just use the first one.
	    if True in matches:
	        first_match_index = matches.index(True)
	        name = known_names[first_match_index]

	    names.append(name)

	    # Draw a box around the face using the Pillow module
	    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

	    # Draw a label with a name below the face
	    text_width, text_height = draw.textsize(name)
	    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
	    draw.text((left + 15, bottom - text_height - 5), name, fill=(255, 255, 255, 255))


	# Remove the drawing library from memory as per the Pillow docs
	del draw

	# Display the resulting image
	pil_image.show()
	pil_image.save("image_with_boxes.jpg")
	print("Finished drawing image")
	return names
