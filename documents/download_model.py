from huggingface_hub import snapshot_download

model_path = snapshot_download(repo_id="Qwen/Qwen2-VL-2B-Instruct", local_dir="./qwen2-vl")
print(f'model file downloaded {model_path}')


