#!/usr/bin/env python3
"""
Pipeline de Download, Otimização WebP e Extração de Fotografias Reais
FFernandes Engenharia e Construção Ltda. (06_FFernandes_Engenharia)
Fonte 100% Oficial: https://ffernandes.eng.br (S3 Locaweb)
"""

import os
import urllib.request
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets" / "img"
S3_BASE = "https://yata-apix-f4834828-c67c-47d4-8f8c-58e2912cb13f.s3-object.locaweb.com.br"

# 1. Mapeamento completo dos 43 arquivos oficiais do site ffernandes.eng.br
OFFICIAL_ASSETS = {
    "brand": {
        "logo-3d.png": "ed4565254d9743cfbef9e8fe352f1e66.png",
        "logo-footer.png": "e59985fed9f54a9c81395ac537c766a2.png",
    },
    "hero": {
        "hero-residencia.png": "15a42a0924e94f479501dae2514f97b4.png",
    },
    "institutional": {
        "nossa-essencia.jpg": "58642fba3f254445a052ee4dbb01c171.jpg",
        "nossos-diferenciais.jpg": "06afa801e95041fab8e4a3dc1cc2c71b.jpg",
        "nossos-servicos.jpg": "2affe9ea4e234ebb808496dc50d38a91.jpg",
        "contato-banner.png": "6af26ede55ff4025abfd0a29e5a85af1.png",
    },
    "portfolio": {
        "prancha-01-condominio-trio.jpg": "a0a81306078c474fa1ca041e944aab65.jpg",
        "prancha-02-heineken-campus.jpg": "9dac2835589041608ae49945aa6f17db.jpg",
        "prancha-03-datacenter-paulinia.png": "f32c3cbddd6a4b4680c02ce98fcdca9d.png",
        "prancha-04-vautier-allbras.png": "2974914484684e1ba20be0afdc2f9f46.png",
        "prancha-05-simba-safari.png": "55e79bdcabde4a379bc8093bb9dae169.png",
        "prancha-06-clube-bayer.png": "4b75bb43cc744196b3eaca41b27bcd99.png",
    },
    "clients": {
        "client-01-atacadao.png": "18a42f135c7641dc88553f9fb8eaeea8.png",
        "client-02-bayer.png": "de721a64934b4ec6ba37f5fad65e2e43.png",
        "client-03-enelpa.png": "e97a779529214e74aab5862a068746e2.png",
        "client-04-toledo-ferrari.png": "85f3489c964b489f98342834df819e60.png",
        "client-05-bombeiros-pmesp.png": "df9e0721dfe7470099090da4d1302a97.png",
        "client-06-assai.png": "664afd64bcff43cea33e4f46f65f48b8.png",
        "client-07-prefeitura-sp.png": "f6d14d7c28464b9d89dbb97c62d3ce8a.png",
        "client-08-cambur.png": "a3b0d62131f44e37b37ccf370b6183b4.png",
        "client-09-drogaria-sp.png": "0ac66ced46024684b6c662e4de437cf5.png",
        "client-10-eversun.png": "50d8358551584ca0826740471dc395b9.png",
        "client-11-helbor.png": "a6fb6838ab0d4b61bf9c51f11d54bdc7.png",
        "client-12-hh-engenharia.png": "1f47c15c75be41d8ac42985f8443618e.png",
        "client-13-irmas-hospitaleiras.png": "c4f3c039036241d1bbc7f3b50867ecc2.png",
        "client-14-jrj-engenharia.png": "608d592d07014519abf661b9de8f6d44.png",
        "client-15-sbn-neurocirurgia.png": "b1c1bb7926954ef1a00dee7febba3a98.png",
        "client-16-drogarias-pacheco.png": "4366506676ad40bdbbf97c1412db193c.png",
        "client-17-mutual-engenharia.png": "856565b31f744276bf3a7b8683fbb123.png",
        "client-18-pague-menos.png": "51be9d4359374946bc116f1a9217445f.png",
        "client-19-planem-engenharia.png": "0e6d6935044a4ead939d68d338741c53.png",
        "client-20-ragazzo.png": "5ce7a104b38b4637b2d95cd7b4cd3297.png",
        "client-21-rmr-engenharia.png": "1ee84a8bd4a6477fa886c9ecb4c84b30.png",
        "client-22-rock-and-ribs.png": "437f7873bd284b418d59421e6a6fcebe.png",
        "client-23-pense-bem-sbn.png": "9980d0bb030e43109d3f052d9877764b.png",
        "client-24-pcon-construtora.png": "c7dc2e86b5194ef694497cb3e7c25780.png",
        "client-25-all-bras-shopping.png": "818be2a9a1d343dfa07c3d1419f9cb1b.png",
        "client-26-shopping-vautier.png": "80d2df095d9c4b6ba486dc60d64e51af.png",
        "client-27-zabo-engenharia.png": "626c34435b3f42628403e571db97d307.png",
        "client-28-enerwatt-engenharia.png": "f21bc86b03ac4a10b29b512831a1489e.png",
        "client-29-bombeiros-viatura.png": "e8ff57ceb4774184aa63371a23cdff93.png",
        "client-30-tael.png": "80c7f4954c2f40f28d8449db76f05926.png",
    },
}


def download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists() or dest.stat().st_size == 0:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            dest.write_bytes(resp.read())


def convert_to_webp(src: Path, quality: int = 88) -> Path:
    webp_path = src.with_suffix(".webp")
    with Image.open(src) as img:
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
        img.save(webp_path, "WEBP", quality=quality, method=6)
    return webp_path


def generate_portfolio_crops() -> None:
    """Extrai as fotografias individuais das 6 pranchas para exibir cards HTML nativos nítidos."""
    port_dir = ASSETS_DIR / "portfolio"
    crops_dir = port_dir / "crops"
    crops_dir.mkdir(parents=True, exist_ok=True)

    crop_specs = [
        # (source_file, output_name, (left, top, right, bottom))
        ("prancha-01-condominio-trio.jpg", "crop-01-condominio-trio.webp", (8, 512, 838, 1036)),
        ("prancha-01-condominio-trio.jpg", "crop-01b-trio-planta.webp", (8, 8, 765, 504)),
        ("prancha-02-heineken-campus.jpg", "crop-02-heineken-campus.webp", (112, 60, 582, 558)),
        ("prancha-02-heineken-campus.jpg", "crop-02b-heineken-aerial.webp", (520, 1480, 882, 1828)),
        ("prancha-02-heineken-campus.jpg", "crop-02c-heineken-lounge.webp", (934, 1406, 1324, 1806)),
        ("prancha-03-datacenter-paulinia.png", "crop-03-datacenter-paulinia.webp", (0, 745, 654, 1918)),
        ("prancha-03-datacenter-paulinia.png", "crop-03b-datacenter-torre.webp", (662, 0, 1358, 492)),
        ("prancha-04-vautier-allbras.png", "crop-04-shopping-vautier.webp", (44, 154, 440, 548)),
        ("prancha-04-vautier-allbras.png", "crop-04b-vautier-fachada2.webp", (448, 156, 758, 546)),
        ("prancha-04-vautier-allbras.png", "crop-05-shopping-allbras.webp", (38, 626, 452, 968)),
        ("prancha-04-vautier-allbras.png", "crop-05b-allbras-obra.webp", (486, 628, 753, 966)),
        ("prancha-05-simba-safari.png", "crop-06-simba-safari.webp", (19, 262, 291, 510)),
        ("prancha-05-simba-safari.png", "crop-06b-simba-entrada.webp", (19, 2, 291, 249)),
        ("prancha-05-simba-safari.png", "crop-06c-simba-recinto.webp", (19, 525, 291, 778)),
        ("prancha-06-clube-bayer.png", "crop-07-clube-bayer.webp", (45, 97, 367, 370)),
        ("prancha-06-clube-bayer.png", "crop-07b-clube-bayer-piscina.webp", (399, 98, 585, 258)),
    ]

    for src_name, out_name, box in crop_specs:
        src_path = port_dir / src_name
        out_path = crops_dir / out_name
        with Image.open(src_path) as img:
            cropped = img.crop(box)
            if cropped.mode not in ("RGB", "RGBA"):
                cropped = cropped.convert("RGB")
            cropped.save(out_path, "WEBP", quality=92, method=6)
            print(f"[CROP] {out_name} ({cropped.size[0]}x{cropped.size[1]})")


def main() -> None:
    total = 0
    for category, files in OFFICIAL_ASSETS.items():
        cat_dir = ASSETS_DIR / category
        cat_dir.mkdir(parents=True, exist_ok=True)
        for local_name, s3_hash in files.items():
            url = f"{S3_BASE}/{s3_hash}"
            dest = cat_dir / local_name
            download_file(url, dest)
            webp_path = convert_to_webp(dest, quality=90 if category in ("brand", "portfolio") else 86)
            with Image.open(dest) as im:
                w, h = im.size
            print(f"[OK] {category}/{local_name} ({w}x{h}) -> {webp_path.name}")
            total += 1

    print(f"\nTotal de assets oficiais baixados e convertidos para WebP: {total}")
    generate_portfolio_crops()


if __name__ == "__main__":
    main()
