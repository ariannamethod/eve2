#!/usr/bin/env python3
"""
Экспортирует текущую модель из процесса обучения.
Загружает чекпоинт и экспортирует в model.bin для использования в чате.
"""

import torch
import sys
from export import load_checkpoint, model_export

def export_current_checkpoint(checkpoint_path="out/ckpt.pt", output_path="out/model.bin"):
    """Экспортирует текущий чекпоинт в model.bin"""
    print(f"📥 Загружаю чекпоинт: {checkpoint_path}")
    try:
        checkpoint = torch.load(checkpoint_path, map_location='cpu')
        iter_num = checkpoint['iter_num']
        val_loss = checkpoint.get('best_val_loss', 'N/A')
        print(f"✅ Чекпоинт загружен: итерация {iter_num}, val loss: {val_loss}")
        
        print(f"🔄 Загружаю модель из чекпоинта...")
        model = load_checkpoint(checkpoint_path)
        
        if model is None:
            print("❌ Не удалось загрузить модель из чекпоинта")
            return False
        
        print(f"💾 Экспортирую модель в: {output_path}")
        model_export(model, output_path, version=0, dtype=torch.float32)
        print(f"✅ Модель экспортирована: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    checkpoint_path = sys.argv[1] if len(sys.argv) > 1 else "out/ckpt.pt"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "out/model.bin"
    
    success = export_current_checkpoint(checkpoint_path, output_path)
    sys.exit(0 if success else 1)

