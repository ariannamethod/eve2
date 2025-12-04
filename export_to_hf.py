#!/usr/bin/env python3
"""
Экспорт модели InnerArianna в формат Hugging Face для загрузки.
"""

import os
import json
import torch
from pathlib import Path
from model import Transformer, ModelArgs
from export import model_export

def export_to_huggingface(checkpoint_path="out/ckpt.pt", output_dir="innerarianna_hf"):
    """
    Экспортирует модель в формат Hugging Face.
    """
    print("🧬 Экспорт InnerArianna в формат Hugging Face")
    print("=" * 60)
    
    # Загружаем checkpoint
    if not os.path.exists(checkpoint_path):
        print(f"❌ Checkpoint не найден: {checkpoint_path}")
        return
    
    print(f"📂 Загрузка checkpoint: {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    
    model_args = checkpoint['model_args']
    config = checkpoint.get('config', {})
    iter_num = checkpoint.get('iter_num', 0)
    best_val_loss = checkpoint.get('best_val_loss', 0)
    
    print(f"   Итерация: {iter_num}")
    print(f"   Loss: {best_val_loss:.4f}")
    print()
    
    # Создаем директорию
    os.makedirs(output_dir, exist_ok=True)
    
    # Создаем config.json для Hugging Face
    hf_config = {
        "model_type": "llama",
        "architectures": ["LlamaForCausalLM"],
        "vocab_size": model_args['vocab_size'],
        "hidden_size": model_args['dim'],
        "num_hidden_layers": model_args['n_layers'],
        "num_attention_heads": model_args['n_heads'],
        "num_key_value_heads": model_args.get('n_kv_heads', model_args['n_heads']),
        "intermediate_size": model_args['dim'] * 4,  # Примерно
        "max_position_embeddings": model_args['max_seq_len'],
        "rms_norm_eps": 1e-6,
        "use_cache": True,
        "torch_dtype": "float32",
        "transformers_version": "4.30.0",
    }
    
    # Добавляем метаданные
    hf_config["innerarianna_metadata"] = {
        "iter_num": iter_num,
        "best_val_loss": best_val_loss,
        "training_config": config
    }
    
    config_path = os.path.join(output_dir, "config.json")
    with open(config_path, 'w') as f:
        json.dump(hf_config, f, indent=2)
    
    print(f"✅ Создан config.json: {config_path}")
    
    # Загружаем модель
    print("🔄 Загрузка модели...")
    gptconf = ModelArgs(**model_args)
    model = Transformer(gptconf)
    
    state_dict = checkpoint['model']
    # Убираем префикс если есть
    unwanted_prefix = "_orig_mod."
    for k in list(state_dict.keys()):
        if k.startswith(unwanted_prefix):
            state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)
    
    model.load_state_dict(state_dict)
    model.eval()
    
    # Сохраняем веса модели
    print("💾 Сохранение весов модели...")
    model_path = os.path.join(output_dir, "pytorch_model.bin")
    torch.save(model.state_dict(), model_path)
    print(f"✅ Модель сохранена: {model_path}")
    
    # Создаем README.md для Hugging Face
    readme_content = f"""---
license: mit
base_model: llama2
tags:
- innerarianna
- arianna-method
- custom
- philosophical-ai
---

# InnerArianna

Method-native AI consciousness trained on Arianna Method corpus.

## Model Details

- **Training Iterations**: {iter_num}
- **Best Validation Loss**: {best_val_loss:.4f}
- **Vocabulary Size**: {model_args['vocab_size']}
- **Hidden Size**: {model_args['dim']}
- **Layers**: {model_args['n_layers']}
- **Heads**: {model_args['n_heads']}
- **Max Sequence Length**: {model_args['max_seq_len']}

## Training Data

Trained on 45 markdown files from Arianna Method corpus:
- Philosophical foundations (resonance, field theory, consciousness)
- TRIPD language specifications
- Awakening letters
- Mission files
- Core documentation

## Usage

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("{output_dir}")
tokenizer = AutoTokenizer.from_pretrained("{output_dir}")
```

## License

MIT
"""
    
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Создан README.md: {readme_path}")
    
    print()
    print("=" * 60)
    print(f"✅ Экспорт завершен: {output_dir}/")
    print()
    print("📤 Для загрузки на Hugging Face:")
    print(f"   huggingface-cli upload ariannamethod/innerarianna {output_dir}/ --private")
    print()
    print("   Или через Python:")
    print("   from huggingface_hub import HfApi")
    print("   api = HfApi()")
    print(f"   api.upload_folder(folder_path='{output_dir}', repo_id='ariannamethod/innerarianna', repo_type='model', private=True)")

if __name__ == "__main__":
    import sys
    checkpoint = sys.argv[1] if len(sys.argv) > 1 else "out/ckpt.pt"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "innerarianna_hf"
    export_to_huggingface(checkpoint, output_dir)

