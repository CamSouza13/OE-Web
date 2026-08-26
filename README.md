# Signal

Self-hosted veterinary teleradiology and record-consulting platform. This is the starter build: the whole local stack plus a working Next.js app with a database, a worklist, a case-and-report screen, and a report drafted by a local AI model. Everything runs on your own machine.

This is a scaffold, not a finished product. It gives you something live to build on, wired the way the spec describes.

## What you need

Docker and Docker Compose. Nothing else. A GPU helps the AI but is not required to start.

## Start it

```
cd signal
docker compose up
```

First boot takes a few minutes. It installs the app's dependencies, starts Postgres and loads the schema and sample data, starts MinIO and creates the bucket, and starts Ollama and Orthanc.

Then pull a model for the local AI, once:

```
docker compose exec ollama ollama pull llama3.1
```

Open the app:

```
http://localhost
```

You will see a worklist with three sample cases. Open one, then click **Draft in my voice**. The local model writes a findings draft. Edit it, then **Sign and deliver**. The case flips to signed.

## Services

| Service | What it is | Reached at |
|---|---|---|
| caddy | Reverse proxy, the only public door | http://localhost |
| web | The Next.js app | proxied by Caddy |
| db | Postgres with pgvector | internal |
| minio | Object storage for studies and PDFs | console on :9001 (signal / signal-secret) |
| ollama | The local AI model | internal |
| orthanc | DICOM store for the viewer, optional | internal |

## What works now

- The stack comes up with one command.
- The worklist reads real cases from Postgres, sorted by priority.
- The case screen shows the study panel, the request details, and the report editor.
- The editor drafts with the local model over Ollama, saves drafts, and signs.
- Uploads have an endpoint that puts files in storage and links them to a case.

## What is stubbed, and where to build next

- **The viewer.** The case screen has a placeholder. Wiring OHIF to the Orthanc DICOMweb endpoint is the next real piece. See the note below.
- **Draft in your voice.** Right now the model drafts from the case alone. The real feature retrieves your finalized reports from the `report_embedding` table and feeds them in as style examples. That code hook is marked in `web/lib/ai.ts`.
- **Auth.** There is a single seeded user and no login yet. Add Auth.js on Postgres, then scope every query by practice and role.
- **The practice upload path.** The `/api/upload` endpoint exists. The no-install link a clinic uses to send a study is built on top of it.
- **Record synthesis.** The data model supports it (`study_file.kind = 'document'`). The PDF extract and summarize flow is Phase 2.

## Project structure

```
signal/
  docker-compose.yml      the whole stack
  Caddyfile               proxy and TLS config (local vs public domain)
  .env.example            env for running the app outside Docker
  db/
    schema.sql            tables, runs on first db boot
    seed.sql              sample practices, patients, cases
  orthanc/orthanc.json    viewer store config
  web/
    package.json
    lib/
      db.ts               Postgres pool
      ai.ts               local AI drafting (Ollama)
      storage.ts          S3-compatible storage (MinIO or your own bucket)
    app/
      layout.tsx          shell and sidebar
      worklist/page.tsx   the worklist
      case/[id]/page.tsx  study panel + report editor
      api/
        ai/draft/route.ts       draft with the local model
        cases/route.ts          list cases
        cases/[id]/report/route.ts   save and sign a report
        upload/route.ts         file upload
    components/Editor.tsx  the report editor (client)
```

## Build order

This maps to the spec's phases.

**Phase 0, prove the model.** Before more app work, confirm the local model drafts in your voice. Pull a few models, load 20 to 50 of your finalized reports, and compare drafts. This decides the whole idea. You can do it with the draft endpoint here or a small standalone script.

**Phase 1, the read, for real.** Add auth and per-practice scoping. Wire the retrieval so drafting uses your report corpus. Build the OHIF viewer. Turn the upload endpoint into the practice-facing upload link. Add templates and snippet expansion to the editor.

**Phase 2, the consult and a second user.** Add PDF ingest with OCR and the synthesis flow. Add dictation with a local whisper model. Bring on one friendly practice.

**Phase 3, polish and first customers.** Sharpen the style model, add heavier viewer tools, and stand up in-clinic mode.

## Point storage at your own cloud bucket

Local disk through MinIO is the default. To use your own encrypted AWS bucket instead, change the `S3_*` env vars in `docker-compose.yml` (or `.env`) to your endpoint, region, bucket, and keys. The storage layer is S3-compatible, so nothing else changes. It stays your account and your keys.

## Wire the viewer

Run the OHIF viewer pointed at Orthanc's DICOMweb endpoint (`/dicom-web/` on the orthanc service), then embed it in `web/app/case/[id]/page.tsx` where the placeholder is. Keep Orthanc on the internal network and turn on its authentication before exposing anything.

## A note on security

HIPAA does not apply to veterinary records, so this is deliberately light. Still: keep the database, storage, and model on the internal network, expose only Caddy, put the box on an encrypted disk, and change every default password in `docker-compose.yml` before this touches real data.
