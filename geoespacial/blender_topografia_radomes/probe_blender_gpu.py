"""Imprime o renderizador GPU efetivamente visível ao Blender/Eevee."""
import gpu

print(f"BLENDER_GPU_VENDOR={gpu.platform.vendor_get()}")
print(f"BLENDER_GPU_RENDERER={gpu.platform.renderer_get()}")
print(f"BLENDER_GPU_VERSION={gpu.platform.version_get()}")
