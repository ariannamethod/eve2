#!/usr/bin/env python3
"""
Принудительно сохраняет чекпоинт из работающего процесса обучения.
Загружает текущий чекпоинт, обновляет его и экспортирует model.bin
"""

import torch
import os
import sys
from export import model_export
from model import ModelArgs, Transformer

def force_save_current_model():
    """Принудительно сохраняет текущую модель"""
    checkpoint_path = "out/ckpt.pt"
    model_bin_path = "out/model.bin"
    
    if not os.path.exists(checkpoint_path):
        print(f"❌ Чекпоинт не найден: {checkpoint_path}")
        return False
    
    print(f"📥 Загружаю чекпоинт: {checkpoint_path}")
    try:
        checkpoint = torch.load(checkpoint_path, map_location='cpu')
        iter_num = checkpoint.get('iter_num', 0)
        best_val_loss = checkpoint.get('best_val_loss', float('inf'))
        model_args = checkpoint['model_args']
        config = checkpoint.get('config', {})
        
        print(f"✅ Чекпоинт загружен:")
        print(f"   Итерация: {iter_num}")
        print(f"   Val loss: {best_val_loss:.4f}")
        
        # Загружаем модель
        print(f"🔄 Загружаю модель...")
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
        
        # Экспортируем model.bin
        print(f"💾 Экспортирую модель в: {model_bin_path}")
        model_export(model, model_bin_path, version=0, dtype=torch.float32)
        
        print(f"✅ Модель экспортирована!")
        print(f"   Теперь можно использовать: python3 chat.py {model_bin_path} -z data/tok4096.bin")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = force_save_current_model()
    sys.exit(0 if success else 1)

