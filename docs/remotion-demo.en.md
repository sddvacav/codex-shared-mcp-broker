# Remotion Demo Video

Public stage: `0.07`

This stage turns the launch story into a real Remotion animation.

## Local Capability Decision

The requested workflow is Remotion-first:

- use Remotion for the animation timeline;
- use repository SVG and Image2 assets as brand material;
- use `staticFile()` and Remotion `<Img>` for assets;
- keep output privacy-safe and reproducible.

No separate built-in Remotion MCP tool was exposed in this session, so the implementation is a standard Remotion project inside the repository.

## Rendered Assets

- MP4: `assets/remotion/codex-shared-mcp-demo.mp4`
- Poster: `assets/remotion/codex-shared-mcp-demo-poster.png`

## Commands

Install dependencies:

```powershell
npm install
```

Preview:

```powershell
npm run video:preview
```

Render poster:

```powershell
npm run video:still
```

Render MP4:

```powershell
npm run video:render
```

## Animation Structure

The composition is `CodexSharedMcpDemo`.

Timeline:

1. Hero: project title and stage.
2. Problem: later Codex windows can slow down.
3. Pattern: shared local HTTP MCP broker.
4. Toolchain: diagnose, benchmark, privacy guard.
5. Benchmark: 80 synthetic units to 9.
6. Privacy: pre-release guard.
7. Close: repo link and scope.

## Privacy Rules

- No private machine path appears in the video.
- No account ID appears in the video.
- No token appears in the video.
- Benchmark data is synthetic.
- Claims stay bounded to Windows + Codex Desktop + MCP fan-out.
