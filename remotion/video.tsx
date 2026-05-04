import React from 'react';
import {
  AbsoluteFill,
  Img,
  Series,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const colors = {
  bg: '#f8fafc',
  ink: '#0f172a',
  muted: '#475569',
  blue: '#2563eb',
  green: '#16a34a',
  red: '#dc2626',
  amber: '#d97706',
  panel: 'rgba(255,255,255,0.92)',
};

const safe = {
  extrapolateLeft: 'clamp' as const,
  extrapolateRight: 'clamp' as const,
};

const steps = [
  {label: 'Problem', detail: 'MCP stdio fan-out slows later windows', color: colors.red},
  {label: 'Pattern', detail: 'Route tools through shared HTTP MCP', color: colors.blue},
  {label: 'Diagnose', detail: 'Check config, transport, broker reachability', color: '#0f766e'},
  {label: 'Benchmark', detail: '80 synthetic units → 9 broker-owned units', color: colors.amber},
  {label: 'Privacy', detail: 'Scan release artifacts before publishing', color: colors.green},
];

const Container: React.FC<{children: React.ReactNode}> = ({children}) => (
  <AbsoluteFill
    style={{
      background:
        'linear-gradient(135deg, #f8fafc 0%, #eef2ff 42%, #ecfeff 100%)',
      fontFamily: 'Inter, Segoe UI, Arial, sans-serif',
      color: colors.ink,
    }}
  >
    {children}
  </AbsoluteFill>
);

const Header: React.FC<{eyebrow: string; title: string; subtitle: string}> = ({
  eyebrow,
  title,
  subtitle,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const y = interpolate(frame, [0, fps], [24, 0], safe);
  const opacity = interpolate(frame, [0, 18], [0, 1], safe);
  return (
    <div style={{position: 'absolute', top: 74 + y, left: 96, opacity}}>
      <div style={{fontSize: 28, color: colors.blue, fontWeight: 700, marginBottom: 20}}>
        {eyebrow}
      </div>
      <div style={{fontSize: 82, lineHeight: 0.95, fontWeight: 800, maxWidth: 1100}}>
        {title}
      </div>
      <div style={{fontSize: 30, lineHeight: 1.35, color: colors.muted, marginTop: 28, maxWidth: 1120}}>
        {subtitle}
      </div>
    </div>
  );
};

const Card: React.FC<{
  children: React.ReactNode;
  left: number;
  top: number;
  width: number;
  height: number;
}> = ({children, left, top, width, height}) => {
  return (
    <div
      style={{
        position: 'absolute',
        left,
        top,
        width,
        height,
        background: colors.panel,
        border: '1px solid rgba(148,163,184,0.45)',
        borderRadius: 24,
        boxShadow: '0 24px 70px rgba(15,23,42,0.12)',
        overflow: 'hidden',
      }}
    >
      {children}
    </div>
  );
};

const HeroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const logoScale = spring({frame, fps: 30, config: {damping: 16}});
  return (
    <Container>
      <Header
        eyebrow="Codex Shared MCP Broker"
        title="Keep xhigh reasoning. Fix local MCP fan-out."
        subtitle="A privacy-safe launch demo for diagnose → benchmark → privacy guard."
      />
      <div
        style={{
          position: 'absolute',
          right: 120,
          top: 190,
          width: 520,
          height: 520,
          transform: `scale(${logoScale})`,
        }}
      >
        <Img src={staticFile('remotion-assets/logo.svg')} style={{width: '100%', height: '100%'}} />
      </div>
      <div style={{position: 'absolute', bottom: 82, left: 96, fontSize: 28, color: colors.muted}}>
        Public stage 0.07 · Remotion animation
      </div>
    </Container>
  );
};

const ProblemScene: React.FC = () => {
  const frame = useCurrentFrame();
  const fill = interpolate(frame, [10, 70], [0, 1], safe);
  return (
    <Container>
      <Header
        eyebrow="Problem"
        title="The model may not be the slow part."
        subtitle="Multiple windows can multiply local MCP stdio tool trees."
      />
      <Card left={116} top={500} width={1688} height={300}>
        <div style={{display: 'flex', height: '100%', alignItems: 'center', gap: 32, padding: 42}}>
          {Array.from({length: 10}).map((_, index) => (
            <div key={index} style={{width: 128, height: 180, borderRadius: 18, background: '#fee2e2', border: '1px solid #fecaca'}}>
              <div style={{height: 38, background: colors.red, borderRadius: '18px 18px 0 0'}} />
              <div style={{padding: 14, fontSize: 18, color: '#7f1d1d'}}>Window {index + 1}</div>
              <div style={{margin: 14, width: 90 * fill, height: 14, background: '#f87171', borderRadius: 99}} />
              <div style={{margin: 14, width: 70 * fill, height: 14, background: '#fca5a5', borderRadius: 99}} />
            </div>
          ))}
        </div>
      </Card>
    </Container>
  );
};

const PatternScene: React.FC = () => {
  return (
    <Container>
      <Header
        eyebrow="Pattern"
        title="Move MCP backends behind one local HTTP broker."
        subtitle="Codex windows connect to shared endpoints instead of spawning repeated stdio trees."
      />
      <Card left={220} top={430} width={1480} height={430}>
        <Img src={staticFile('remotion-assets/architecture.en.svg')} style={{width: '100%', height: '100%', objectFit: 'contain', padding: 30}} />
      </Card>
    </Container>
  );
};

const FlowScene: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Container>
      <Header
        eyebrow="Toolchain"
        title="Diagnose → benchmark → privacy guard."
        subtitle="The demo is built around evidence that can be shared safely."
      />
      <div style={{position: 'absolute', left: 120, top: 440, display: 'flex', gap: 28}}>
        {steps.map((step, index) => {
          const opacity = interpolate(frame, [index * 12, index * 12 + 18], [0.2, 1], safe);
          return (
            <div key={step.label} style={{width: 320, height: 280, borderRadius: 24, background: colors.panel, border: '1px solid #cbd5e1', padding: 30, opacity}}>
              <div style={{width: 58, height: 58, borderRadius: 99, background: step.color, color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 28, fontWeight: 800}}>
                {index + 1}
              </div>
              <div style={{fontSize: 34, fontWeight: 800, marginTop: 28}}>{step.label}</div>
              <div style={{fontSize: 22, color: colors.muted, marginTop: 18, lineHeight: 1.35}}>{step.detail}</div>
            </div>
          );
        })}
      </div>
    </Container>
  );
};

const BenchmarkScene: React.FC = () => {
  return (
    <Container>
      <Header
        eyebrow="Synthetic benchmark"
        title="80 process units become 9 broker-owned units."
        subtitle="The benchmark explains local process ownership. It is not a model intelligence benchmark."
      />
      <Card left={250} top={400} width={1420} height={500}>
        <Img src={staticFile('remotion-assets/benchmark.en.svg')} style={{width: '100%', height: '100%', objectFit: 'contain'}} />
      </Card>
    </Container>
  );
};

const PrivacyScene: React.FC = () => {
  return (
    <Container>
      <Header
        eyebrow="Privacy"
        title="Public artifacts are scanned before release."
        subtitle="The guard flags tokens, private paths, local gateway names, runtime traces, and risky files."
      />
      <Card left={220} top={460} width={1480} height={320}>
        <div style={{padding: 42, fontFamily: 'Cascadia Mono, Consolas, monospace', fontSize: 30, lineHeight: 1.55, color: '#14532d'}}>
          <div>&gt; agent-runtime-privacy-guard .</div>
          <div style={{marginTop: 22}}>Status: PASS</div>
          <div>No configured secret or private runtime patterns were detected.</div>
          <div style={{color: colors.muted}}>Matched secret values are never printed.</div>
        </div>
      </Card>
    </Container>
  );
};

const CloseScene: React.FC = () => {
  return (
    <Container>
      <Header
        eyebrow="Release-safe agent runtime toolkit"
        title="Narrow scope. Clear evidence. Privacy-safe launch."
        subtitle="Windows + Codex Desktop + MCP fan-out + shared local HTTP broker + validation."
      />
      <Card left={360} top={475} width={1200} height={250}>
        <div style={{padding: 42, fontSize: 34, lineHeight: 1.45}}>
          <div style={{fontWeight: 800}}>github.com/sddvacav/codex-shared-mcp-broker</div>
          <div style={{color: colors.muted, marginTop: 24}}>diagnose · benchmark · privacy guard · Remotion demo</div>
        </div>
      </Card>
    </Container>
  );
};

export const CodexSharedMcpDemo: React.FC = () => {
  return (
    <AbsoluteFill>
      <Series>
        <Series.Sequence durationInFrames={36}>
          <HeroScene />
        </Series.Sequence>
        <Series.Sequence durationInFrames={36}>
          <ProblemScene />
        </Series.Sequence>
        <Series.Sequence durationInFrames={36}>
          <PatternScene />
        </Series.Sequence>
        <Series.Sequence durationInFrames={36}>
          <FlowScene />
        </Series.Sequence>
        <Series.Sequence durationInFrames={36}>
          <BenchmarkScene />
        </Series.Sequence>
        <Series.Sequence durationInFrames={36}>
          <PrivacyScene />
        </Series.Sequence>
        <Series.Sequence durationInFrames={36}>
          <CloseScene />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};
