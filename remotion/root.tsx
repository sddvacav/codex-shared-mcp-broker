import React from 'react';
import {Composition} from 'remotion';
import {CodexSharedMcpDemo} from './video';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="CodexSharedMcpDemo"
      component={CodexSharedMcpDemo}
      durationInFrames={252}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{}}
    />
  );
};
