from main_drum import generate_random_loop, visualize_loop_image

loop = generate_random_loop("detroit",16)
img_buffer = visualize_loop_image(loop)

with open("test_pattern.png","wb") as f:
    f.write(img_buffer.getvalue())
print("pic save is test_pattern.png")