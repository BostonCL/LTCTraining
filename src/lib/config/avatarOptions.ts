export interface AvatarOption {
  id: string;
  name: string;
  description: string;
  url: string;
  type: 'ready-player-me' | 'live2d' | 'custom';
  features: string[];
  preview?: string;
}

export const avatarOptions: AvatarOption[] = [
  {
    id: 'ready-player-me-1',
    name: 'Professional Host',
    description: 'A professional-looking avatar with realistic facial animations and lip-sync',
    url: 'https://models.readyplayer.me/64f7b8b8b8b8b8b8b8b8b8b.glb',
    type: 'ready-player-me',
    features: ['Lip-sync', 'Facial expressions', '3D rendering', 'Professional appearance'],
    preview: '/images/avatars/professional-host.jpg'
  },
  {
    id: 'ready-player-me-2', 
    name: 'Friendly Instructor',
    description: 'A friendly, approachable avatar perfect for educational content',
    url: 'https://models.readyplayer.me/64f7b8b8b8b8b8b8b8b8b8c.glb',
    type: 'ready-player-me',
    features: ['Lip-sync', 'Friendly expressions', '3D rendering', 'Educational style'],
    preview: '/images/avatars/friendly-instructor.jpg'
  },
  {
    id: 'live2d-1',
    name: 'Anime Style Host',
    description: 'A cute anime-style character with smooth 2D animations',
    url: '/models/live2d/host.model3.json',
    type: 'live2d',
    features: ['2D animations', 'Anime style', 'Smooth movements', 'Lightweight'],
    preview: '/images/avatars/anime-host.jpg'
  },
  {
    id: 'custom-basketball',
    name: 'Enhanced Basketball',
    description: 'An improved version of the basketball with better facial animations',
    url: 'custom',
    type: 'custom',
    features: ['Simple design', 'Fast loading', 'Basketball theme', 'Easy customization'],
    preview: '/images/avatars/enhanced-basketball.jpg'
  }
];

export const defaultAvatar = avatarOptions[0];

// Avatar animation presets
export const animationPresets = {
  talking: {
    mouthOpen: true,
    eyebrowRaise: true,
    eyeMovement: true,
    headNod: true
  },
  idle: {
    breathing: true,
    eyeBlink: true,
    subtleMovement: true
  },
  listening: {
    focused: true,
    slightTilt: true,
    eyeContact: true
  }
};
