# GitHub'a Yayınlama Rehberi

Bu klasördeki her şey paylaşıma hazır. Bu rehber, repo'yu GitHub'a aktarmak için adım adım komutları içerir. Toplam süre: **15-20 dakika**.

---

## Önkoşullar

- [ ] GitHub hesabın var (yoksa github.com'dan aç)
- [ ] Bilgisayarda **Git** kurulu (yoksa: https://git-scm.com/download/win)
- [ ] Kontrol: cmd'de `git --version` → `git version 2.x.x` görmelisin

Yoksa kur, devam et.

---

## Adım 1: Vault'unu temizle (paylaşmadan ÖNCE)

GitHub'a kişisel notlarını koymamak için, önce vault'undaki "of", "may", "into" gibi anlamsız kayıtları sil:

```cmd
cd "C:\Users\Muhammet\Desktop\Ingilizce-Kelimeler\Ingilizce-Kelimeler\Araçlar"
python vault_temizle.py
```

Bu komut sadece **listeler**, silmez. Listeyi gör, "evet bunlar gitsin" dediğinde:

```cmd
python vault_temizle.py --sil
```

`evet` yazıp Enter → hepsi siler. `sec` yazıp tek tek seçebilirsin de.

---

## Adım 2: GitHub'da repo aç

1. https://github.com → sağ üstte **+** → **New repository**
2. Repository name: `ingilizce-kelimeler` (veya istediğin)
3. Description: `Auto-generated English vocabulary cards for Obsidian, with Turkish translations`
4. **Public** seç (paylaşacaksan)
5. ⚠️ **README, .gitignore, license eklemiyorsun** — onlar bizde zaten var. Boş repo olarak başlat.
6. **Create repository**

GitHub sana yeşil ekranda komutları gösterir. Bizim ihtiyacımız olan iki satır oradadır:
```
https://github.com/<seninkullaniciadin>/ingilizce-kelimeler.git
```

Bu URL'i kopyala.

---

## Adım 3: Repo'yu git ile başlat

Cmd'yi `_GitHub_Repo/` klasöründe aç:

```cmd
cd "C:\Users\Muhammet\Desktop\Ingilizce-Kelimeler\Ingilizce-Kelimeler\_GitHub_Repo"
```

Komutları sırayla çalıştır:

```cmd
git init
git add .
git commit -m "İlk versiyon: Obsidian vocabulary auto-generator"
git branch -M main
git remote add origin https://github.com/<seninkullaniciadin>/ingilizce-kelimeler.git
git push -u origin main
```

> `<seninkullaniciadin>` yerine gerçek GitHub kullanıcı adını yaz.

`git push` adımında GitHub kullanıcı adı + parola/token sorabilir. Modern GitHub parolayı kabul etmiyor — Personal Access Token gerekiyor:

1. github.com → sağ üstte profil → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
2. "repo" yetkisini ver, 30 gün süre yeterli
3. Token'ı kopyala (sadece bir kez gösterilir)
4. `git push`'ta parola sorulduğunda token'ı yapıştır

Bir kez yapacaksın, sonrası `git push` hatırlar.

---

## Adım 4: README'yi son kontrol et

Tarayıcıda repo'na git: `https://github.com/<seninkullaniciadin>/ingilizce-kelimeler`

Şunlara bak:
- [ ] README.md ana sayfada düzgün render oldu mu? (Headerlar, kod blokları, tablolar)
- [ ] LICENSE üst tarafta "MIT License" olarak görünüyor mu?
- [ ] Klasör yapısı doğru mu? (Templates/, Araçlar/, Kelimeler/, docs/)
- [ ] `<your-user>` placeholder'ları gerçek kullanıcı adınla değiştirildi mi?

Eğer placeholder kaldıysa local'de düzelt, tekrar push:

```cmd
git add .
git commit -m "Fix: replace placeholder with real GitHub username"
git push
```

---

## Adım 5: Repo metadata'sı (ARAMADA BULUNMAK İÇİN ŞART)

GitHub'da repo'na git, sağ tarafta **About** kısmında dişli ikonu → **Edit repository details**:

- Description: `Auto-generated English vocabulary cards for Obsidian, with Turkish translations`
- Website: (boş bırak veya kişisel sitende gösteriyorsan ekle)
- Topics: şunları tek tek ekle (her biri ayrı tag):
  - `obsidian`
  - `obsidian-md`
  - `vocabulary`
  - `english-learning`
  - `turkish`
  - `language-learning`
  - `flashcards`
  - `spaced-repetition`
  - `python`
  - `wiktionary`

Topics önemli — GitHub'ın arama keşfini büyük oranda buradan yapıyor.

---

## Adım 6: Demo GIF'i ekle

Şu an `docs/demo.gif` mevcut değil — README'de placeholder olarak gösteriliyor. Kayıt için: [docs/RECORDING.md](docs/RECORDING.md)

Kaydı yapıp `docs/demo.gif` olarak yerleştirdikten sonra:

```cmd
git add docs/demo.gif
git commit -m "docs: add demo GIF"
git push
```

README artık GIF'i gösterecek.

---

## Adım 7: İlk paylaşım

[docs/LINKEDIN_POST.md](docs/LINKEDIN_POST.md) dosyasında hazır taslaklar var. Önerilen sıra:

1. **LinkedIn TR post** — taslağı kopyala, `<REPO_URL>` yerine gerçek URL'yi koy, GIF'i ekle, paylaş
2. **24 saat bekle** — engagement'a bak
3. **Reddit r/ObsidianMD** — İngilizce taslak, aynı GIF
4. **Twitter/X** — kısa versiyon, hem TR hem EN
5. **Gerekirse** Hacker News "Show HN" — ana sayfaya çıkma şansı düşük ama "new" akışında 1-2 hafta görünür

---

## Hatalar ve çözümleri

**`git push` "rejected — non-fast-forward"**
GitHub'da repo açarken yanlışlıkla README oluşturduysan local ile uyumsuz. Çözüm:
```cmd
git pull origin main --allow-unrelated-histories
git push
```

**`git push` "Authentication failed"**
Token yanlış girilmiş. Yukarıdaki Adım 3'teki Personal Access Token kısmına dön.

**README bozuk render oluyor**
Markdown sözdizimi hatası olabilir. GitHub'ın render'ı çoğu hatayı yakalar — local'de düzelt, push.

**Türkçe karakterli klasör adları sorun çıkardı**
`Şablon - Orta.md` gibi dosya adları bazen Windows ↔ Linux ↔ macOS arasında bozuluyor. Repo public olduğunda farklı işletim sistemi kullanan birinin sorun yaşaması mümkün. Şimdilik yaşa, raporlanırsa İngilizce'ye çevirirsin.

---

## Sonraki adımlar (opsiyonel)

- [ ] `docs/demo.gif` ekle
- [ ] LinkedIn'de paylaş
- [ ] Reddit'te paylaş
- [ ] Vatandaşlık sözleşmesi (CONTRIBUTING.md) zaten var — okuyanlar görür
- [ ] İlk PR geldiğinde sıcak karşıla, küçük taklitler bile teşvik et
- [ ] Bir ay sonra: kullanım istatistiklerine bak (yıldız, fork, issue), neyin işe yaradığını öğren

---

İyi şanslar. Bir yerde takılırsan komut çıktısını yapıştır, beraber bakarız.
