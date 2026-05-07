# Paper Graph Reader

A Vercel-hosted reading site for graphified papers.

## Add a future graphified paper

Preferred import flow:

```bash
python scripts/import_graphified_paper.py /root/graphified-papers/arxiv-2604.26615 --id 2604.26615
npm test && npm run build
git add . && git commit -m "Add graphified paper 2604.26615" && git push
vercel deploy --prod --yes --token "$VERCEL_TOKEN"
```

Manual flow:
1. Put the graphified paper folder under `public/papers/<paper-id>/`.
2. Add/update `public/papers/index.json` with its metadata and asset paths.
3. Run `npm test && npm run build`.
4. Commit, push, and redeploy to Vercel.

Current paper: arXiv 2604.26615.
