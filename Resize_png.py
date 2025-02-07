from PIL import Image

# Abrir a imagem
imagem = Image.open("color.png")

# Redimensionar para 192x192
imagem_resized = imagem.resize((32, 32), Image.LANCZOS)

# Sobrescrever o arquivo original
imagem_resized.save("outline.png")

print("Imagem redimensionada e sobrescrita com sucesso!")
