# Digital Garden Setup Guide
*Complete setup instructions for jonathannguyen.net with Cloudflare Pages*

## 🎯 What This Gives You

✅ **Perfect title control** - Navigation shows proper titles, not slugs  
✅ **Obsidian workflow** - Keep writing in Obsidian exactly as you do now  
✅ **Beautiful URLs** - `/daily-planning-system/` instead of filename mess  
✅ **Wikilink support** - [[Links]] work perfectly  
✅ **Graph visualization** - See connections between your notes  
✅ **Lightning fast** - Cloudflare global CDN  
✅ **$0/month hosting** - Free tier is generous  

## 🏗 Architecture

```
Obsidian Vault → GitHub Actions → Jekyll Build → Cloudflare Pages
```

## 📋 Setup Checklist

### 1. GitHub Repository Setup
- [ ] Push this repository to GitHub as `jonathan-nguyen/jonathannguyen-net-jekyll`
- [ ] Set up GitHub secrets (see below)
- [ ] Test local build works

### 2. Cloudflare Pages Setup  
- [ ] Create Cloudflare account
- [ ] Connect GitHub repository
- [ ] Configure build settings
- [ ] Set up custom domain

### 3. Obsidian Vault Integration
- [ ] Set up Obsidian vault repository (optional but recommended)
- [ ] Configure sync workflow
- [ ] Test publishing workflow

## 🔧 Detailed Setup Instructions

### Step 1: GitHub Repository
```bash
cd /Users/jonathan/GitHub/personal/jonathannguyen-net-jekyll
git remote add origin https://github.com/jonathan-nguyen/jonathannguyen-net-jekyll.git
git add .
git commit -m "🚀 Initial Jekyll Digital Garden setup"
git push -u origin main
```

### Step 2: GitHub Secrets Configuration
In your GitHub repository settings, add these secrets:

**Required for Cloudflare deployment:**
- `CLOUDFLARE_API_TOKEN`: Your Cloudflare API token
- `CLOUDFLARE_ACCOUNT_ID`: Your Cloudflare account ID  
- `CLOUDFLARE_ZONE_ID`: Your domain's zone ID (for cache purging)

**Optional for Obsidian auto-sync:**
- `OBSIDIAN_VAULT_TOKEN`: GitHub personal access token for vault access

### Step 3: Cloudflare Pages Setup

1. **Create Cloudflare account** at https://dash.cloudflare.com
2. **Go to Pages** → **Create a project** → **Connect to Git**
3. **Select your repository**: `jonathan-nguyen/jonathannguyen-net-jekyll`
4. **Configure build settings**:
   - **Framework preset**: Jekyll
   - **Build command**: `./cloudflare-build.sh`
   - **Build output directory**: `_site`
   - **Root directory**: `/` (leave empty)

5. **Environment variables** (in Cloudflare Pages settings):
   ```
   JEKYLL_ENV=production
   RUBY_VERSION=3.1
   ```

6. **Custom domain setup**:
   - Add `jonathannguyen.net` as custom domain
   - Update DNS to point to Cloudflare Pages

### Step 4: Local Development Setup

```bash
# Install dependencies
bundle install

# Sync from Obsidian
python scripts/obsidian-sync.py

# Serve locally
bundle exec jekyll serve --livereload

# Visit http://localhost:4000
```

## 📝 Publishing Workflow

### From Obsidian (Your Current Workflow)
1. **Write in Obsidian** as you normally do
2. **Add frontmatter** to notes you want to publish:
   ```yaml
   ---
   title: "My Amazing Post"
   nav_title: "Amazing Post"  # Shorter for navigation
   publish: true              # Set to false to hide
   tags: [startup, productivity]
   ---
   ```
3. **Automatic sync** happens every 6 hours via GitHub Actions
4. **Manual sync** anytime: Run the GitHub Action or push to trigger

### Manual Publishing (Alternative)
```bash
# Sync latest from Obsidian
python scripts/obsidian-sync.py

# Test locally
bundle exec jekyll serve

# Commit and push
git add .
git commit -m "📝 New posts"
git push
```

## 🎨 Customization Options

### Theme Customization
Edit these files to customize appearance:
- `_sass/_style.scss` - Main styles
- `_layouts/note.html` - Note page layout
- `_includes/` - Reusable components

### Navigation Customization
The sync script automatically creates clean navigation titles:
- **Full title**: "My Daily Planning System"  
- **Nav title**: "Daily Planning System"
- **URL slug**: `/daily-planning-system/`

### Adding New Features
The digital garden theme supports:
- **Graph view**: Visual connections between notes
- **Backlinks**: Automatic bidirectional linking
- **Search**: Built-in note search
- **Tags**: Organize by topics

## 🔗 Key URLs After Setup

- **Live site**: https://jonathannguyen.net
- **GitHub repo**: https://github.com/jonathan-nguyen/jonathannguyen-net-jekyll
- **Cloudflare dashboard**: https://dash.cloudflare.com
- **Graph view**: https://jonathannguyen.net/graph (once deployed)

## 🚨 Troubleshooting

### Build Failures
1. Check GitHub Actions logs
2. Test locally: `bundle exec jekyll build`
3. Ensure all dependencies in Gemfile

### Sync Issues  
1. Verify Obsidian vault path in sync script
2. Check frontmatter formatting
3. Run sync manually: `python scripts/obsidian-sync.py`

### Cloudflare Issues
1. Check build logs in Cloudflare Pages
2. Verify environment variables
3. Test build command locally

## 🎯 Next Steps After Setup

1. **Customize theme** colors and typography
2. **Add more notes** to see graph connections
3. **Set up analytics** (Cloudflare Web Analytics is free)
4. **Configure redirects** from old Obsidian Publish URLs
5. **Add contact form** using Cloudflare Pages Functions

## 📊 Performance Expectations

- **Build time**: ~30 seconds
- **Global load time**: <500ms via Cloudflare CDN  
- **Lighthouse score**: 95+ across all metrics
- **SEO**: Fully optimized with proper meta tags

## 🔄 Migration from Obsidian Publish

1. **Test new site** thoroughly on staging domain
2. **Set up redirects** in `_redirects` file
3. **Update DNS** to point to Cloudflare Pages
4. **Cancel Obsidian Publish** subscription
5. **Monitor** for any issues

---

**🎉 You're all set!** Your digital garden will have professional navigation, beautiful URLs, and seamless Obsidian integration while costing $0/month to host.