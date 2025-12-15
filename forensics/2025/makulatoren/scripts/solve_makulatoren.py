import subprocess
import os

try:
    from PIL import Image, ImageOps, ImageEnhance
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

def solve():
    # The correct sequence derived from analysis
    chain = ["19", "3", "11", "21", "13", "4", "14", "17", "15"]
    
    print(f"[*] Assembling chain: {chain}")
    data = b""
    for f in chain:
        with open(f, 'rb') as file:
            data += file.read()
            
    # Write the full image
    output_filename = "solution.jpg"
    with open(output_filename, "wb") as f:
        f.write(data)
    print(f"[+] Created {output_filename}")
        
    # Verify via djpeg and OCR
    # 1. Convert to PPM (djpeg handles potential stream errors gracefully)
    ppm_filename = "solution.ppm"
    subprocess.run(["djpeg", "-grayscale", "-pnm", "-outfile", ppm_filename, output_filename], stderr=subprocess.DEVNULL)
    
    if not os.path.exists(ppm_filename):
        print("[-] Error: djpeg failed to produce output.")
        return

    # 2. Process image (Invert colors + increase contrast)
    # Use ImageMagick `convert` if available; otherwise fall back to Pillow.
    processed_filename = "processed.png"

    def imagemagick_convert_exists() -> bool:
        from shutil import which
        return which("convert") is not None
    def imagemagick_magick_exists() -> bool:
        from shutil import which
        return which("magick") is not None

    def preprocess(cmd_base, out):
        subprocess.run(cmd_base + [out], check=True)

    if imagemagick_magick_exists():
        # Preferred pipeline per manual test:
        # magick solution.ppm -colorspace Gray -resize 300% -deskew 40% -clahe 20x20+10%+2 -contrast-stretch 10% processed.png
        preprocess([
            "magick", ppm_filename,
            "-colorspace", "Gray",
            "-resize", "300%",
            "-deskew", "40%",
            "-clahe", "20x20+10%+2",
            "-contrast-stretch", "10%",
        ], processed_filename)
        print(f"[+] Processed image saved to {processed_filename} (ImageMagick v7 'magick')")
    elif imagemagick_convert_exists():
        # Fallback pipeline for IM6 convert
        preprocess([
            "convert", ppm_filename,
            "-colorspace", "Gray",
            "-resize", "300%",
            "-deskew", "40%",
            "-clahe", "20x20+10%+2",
            "-contrast-stretch", "10%",
        ], processed_filename)
    elif PIL_AVAILABLE:
        # Pillow pipeline: open PPM, invert, and boost contrast
        try:
            img = Image.open(ppm_filename)
            img = ImageOps.invert(img.convert("RGB"))
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)  # modest contrast boost
            img.save(processed_filename)
            print(f"[+] Processed image saved to {processed_filename} (Pillow)")
        except Exception as e:
            print(f"[-] Pillow processing failed: {e}")
            return
    else:
        print("[-] Neither ImageMagick nor Pillow is available. Install one of:\n"
              "    brew install imagemagick\n"
              "    or pip install pillow")
        return

        # OCR step removed; final result is visible in processed image
        print("[*] Review the processed image manually for the final flag.")

if __name__ == "__main__":
    solve()
