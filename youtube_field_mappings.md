# YouTube Upload Module Field Configuration

## Required Fields Configuration

### 1. Connection*
- **Field**: Connection
- **Value**: Select your existing YouTube connection or create a new one
- **Note**: You need to authenticate with Google/YouTube first

### 2. Title*
- **Field**: Title
- **Mapping**: `{{20.youtubeTitle}}`
- **Alternative**: `{{17.videoTitle}}` (if you want to use the webhook title directly)
- **Constraints**: 
  - Max 100 characters
  - Remove < and > characters if present
- **Current Value**: "EspaLuz Success Story"

### 3. File Configuration

#### File Name*
- **Field**: File → filename
- **Mapping**: `{{17.videoTitle}}.mp4`
- **Alternative**: `EspaLuz_{{formatDate(now; "YYYYMMDD_HHmmss")}}.mp4`
- **Note**: Must not be empty

#### Data*
- **Field**: File → data
- **Mapping**: `https://dl.dropboxusercontent.com/scl/fi/uy5uv35wicmtbcr667p9u/202509151508.mp4`
- **Note**: Use the direct download link we created earlier
- **Dynamic Option**: `{{17.videoURL}}` (if your webhook provides different video URLs)

### 4. Video Category*
- **Field**: categoryId
- **Recommended Value**: `22` (People & Blogs)
- **Other Options**:
  - `26` - Howto & Style
  - `27` - Education
  - `24` - Entertainment
  - `25` - News & Politics

### 5. Privacy Status and Scheduling*
- **Field**: privacyStatus
- **Options**:
  - `public` - Anyone can search for and view
  - `unlisted` - Anyone with the link can view
  - `private` - Only you can view
  - `scheduled` - Set a future publish date
- **Recommended**: `public` for promotional content

### 6. Description
- **Field**: description
- **Mapping**: 
```
{{20.smartContent}}

🌟 Transform your life with EspaLuz
💬 Connect with us: https://wa.me/50766623757

{{17.hashtags}}

#EspaLuz #Transformation #PersonalGrowth #SuccessStory
```
- **Constraints**: 
  - Max 5000 characters
  - Remove < and > characters if present

### 7. The video is made for kids
- **Field**: madeForKids
- **Value**: `false` (No)
- **Note**: Set to true only if content is specifically designed for children under 13

### 8. The video contains altered/synthetic media
- **Field**: containsAlteredMedia
- **Value**: `false` (No)
- **Note**: Set to true if video contains AI-generated or heavily edited content

## Complete Module Configuration

```json
{
    "id": 1,
    "module": "youtube:uploadVideo",
    "version": 4,
    "parameters": {
        "connection": "your_youtube_connection_id"
    },
    "mapper": {
        "title": "{{20.youtubeTitle}}",
        "file": {
            "filename": "{{if(17.videoTitle; 17.videoTitle; \"EspaLuz_Video\")}}.mp4",
            "data": "https://dl.dropboxusercontent.com/scl/fi/uy5uv35wicmtbcr667p9u/202509151508.mp4"
        },
        "categoryId": "22",
        "privacyStatus": "public",
        "description": "{{20.smartContent}}\n\n🌟 Transform your life with EspaLuz\n💬 Connect with us: https://wa.me/50766623757\n\n{{if(17.hashtags; 17.hashtags; \"#EspaLuz #Transformation\")}}\n\n#PersonalGrowth #SuccessStory",
        "madeForKids": false,
        "containsAlteredMedia": false
    }
}
```

## Step-by-Step Configuration in Make.com

1. **Connection**: Click "Add" next to Connection field and authenticate with YouTube
2. **Title**: Enter `{{20.youtubeTitle}}` in the mapping field
3. **File Name**: Enter `{{17.videoTitle}}.mp4`
4. **File Data**: Enter the direct Dropbox link: `https://dl.dropboxusercontent.com/scl/fi/uy5uv35wicmtbcr667p9u/202509151508.mp4`
5. **Video Category**: Select "People & Blogs" from dropdown
6. **Privacy Status**: Select "Public" from dropdown
7. **Description**: Copy the description template above
8. **Made for Kids**: Select "No"
9. **Contains Altered Media**: Select "No"

## Testing Recommendations

1. Start with `privacyStatus: "private"` for initial testing
2. Use a short test description first
3. Verify the direct download link works
4. Check title length (should be under 100 characters)
5. Once working, change privacy to "public"