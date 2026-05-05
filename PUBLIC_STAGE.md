# Public Stage Numbering

The package uses normal Python semantic versions such as `0.3.0`, `0.4.0`, and `0.5.0`.

For public launch storytelling, the project also uses a simpler stage label:

| Package version | Public stage | Meaning |
| --- | --- | --- |
| `0.3.0` | `0.03` | First shareable benchmark stage |
| `0.4.0` | `0.04` | Cross-client runtime notes stage |
| `0.5.0` | `0.05` | Privacy guard extraction stage |
| `0.6.0` | `0.06` | Short demo and release asset pack stage |
| `0.7.0` | `0.07` | Remotion rendered demo video stage |
| `0.8.0` | `0.08` | Static landing page and material library stage |
| `0.9.0` | `0.09` | Hosted product blueprint stage |
| `0.10.0` | `0.10` | High-concurrency broker sharding stage |

The reason for keeping both:

- Python packaging expects standard versions.
- GitHub releases and pip metadata should remain predictable.
- Public stage labels are easier to read in launch posts and social copy.

Do not encode the public stage as a nonstandard package version.
