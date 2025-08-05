# Development Configuration

This file controls development features that can be easily toggled on/off.

## Location
`src/lib/config/dev.ts`

## Features

### Video Navigation Buttons
- **Setting**: `DEV_FEATURES.showVideoNavigationButtons`
- **Default**: `true`
- **Description**: Shows Previous/Next buttons in the video controls at the bottom of videos
- **Usage**: Set to `false` to hide navigation buttons in production mode

### Debug Logging
- **Setting**: `DEV_FEATURES.enableDebugLogging`
- **Default**: `false`
- **Description**: Enables additional console logging for debugging
- **Usage**: Set to `true` when debugging issues

### Development Info Overlay
- **Setting**: `DEV_FEATURES.showDevInfo`
- **Default**: `false`
- **Description**: Shows development information overlay
- **Usage**: Set to `true` to see development info

### Developer Mode
- **Setting**: `DEV_FEATURES.developerMode`
- **Default**: `true`
- **Description**: Unlocks all slides and bypasses progress restrictions
- **Usage**: Set to `true` to enable developer mode with full access to all content
- **Features**:
  - Bypasses audio progress requirements
  - Allows navigation to any slide/module
  - Shows developer mode indicator in UI
  - Adds quick navigation buttons in sidebar
  - Disables progress saving/loading

## Quick Toggle

To disable all development features for production:
```typescript
export const DEV_MODE = false;
```

To enable all development features:
```typescript
export const DEV_MODE = true;
```

## Individual Feature Control

You can also control individual features:
```typescript
export const DEV_FEATURES = {
  showVideoNavigationButtons: true,  // Show/hide video nav buttons
  enableDebugLogging: false,         // Enable/disable debug logs
  showDevInfo: false,                // Show/hide dev info overlay
  developerMode: true                // Enable/disable developer mode
};
``` 