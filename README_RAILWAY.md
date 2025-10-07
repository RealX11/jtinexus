
# EGEM Readonly Demo (Railway)
Bu repo Railway'de SQLite veritabanını görüntülemek için basit bir Flask + Gunicorn uygulamasıdır.

## Adımlar
1. Bu repo'yu GitHub'a yükle.
2. Railway → New Project → GitHub Repository → repo'yu seç → Deploy.
3. Railway → Add Volume → mount path: /data
4. Volume içine jobs.db dosyanı yükle.
5. Settings → Variables → Add: `DB_PATH=/data/jobs.db`
6. Deploy sonrası çıkan URL: https://<project>.up.railway.app/jobs
