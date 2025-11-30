# 🚀 Vercel Deployment Guide

## Quick Deployment Steps

### 1. Push to GitHub
```bash
cd "/Users/dishant/Desktop/new chat bot/MachineLearning_Algorithms_Dishant-"
git add .
git commit -m "Production ready - Password Manager"
git push origin main
```

### 2. Deploy on Vercel

#### Option A: Vercel Dashboard (Recommended)
1. Go to https://vercel.com/new
2. Click "Import Project"
3. Select your GitHub repository: `Dishant707/MachineLearning_Algorithms_Dishant-`
4. **IMPORTANT:** Set the "Root Directory" to: `email-password-manager`
5. Add Environment Variables (see below)
6. Click "Deploy"

#### Option B: Vercel CLI
```bash
cd email-password-manager
npm i -g vercel
vercel
```

### 3. Environment Variables

Add these in Vercel Project Settings → Environment Variables:

```env
# Required for session management (min 32 characters)
SECRET_COOKIE_PASSWORD=your-secure-random-string-minimum-32-characters

# Your Neon PostgreSQL connection string
DATABASE_URL=postgresql://neondb_owner:npg_sOj8FApKV2Zl@ep-weathered-rice-ad15n02h-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
```

**Important Notes:**
- Use a strong, random string for `SECRET_COOKIE_PASSWORD` (you can generate one at https://1password.com/password-generator/)
- The `DATABASE_URL` should be your Neon PostgreSQL connection string (already configured)
- Both variables must be set for all environments (Production, Preview, Development)

### 4. Verify Deployment

After deployment:
1. Your app will be live at: `https://your-project-name.vercel.app`
2. Test the following:
   - ✅ Registration page works
   - ✅ Login works
   - ✅ Dashboard loads
   - ✅ Can add credentials
   - ✅ Can view/copy passwords
   - ✅ Can delete credentials

### 5. Database Tables

The database tables should already exist in your Neon database from the local setup:
- `users` table
- `credentials` table

If you need to recreate them, you can run:
```sql
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS credentials (
  id SERIAL PRIMARY KEY,
  userId INTEGER NOT NULL,
  service TEXT NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  FOREIGN KEY (userId) REFERENCES users (id) ON DELETE CASCADE
);
```

## Troubleshooting

### Build Errors
- Check that all environment variables are set
- Verify the root directory is set to `email-password-manager`
- Check build logs in Vercel dashboard

### Database Connection Issues
- Verify your Neon database is active
- Check the DATABASE_URL is correct
- Ensure SSL is enabled in your Neon database settings

### Session Issues
- Make sure SECRET_COOKIE_PASSWORD is at least 32 characters
- Check that cookies are enabled in your browser
- Verify HTTPS is enabled (automatic on Vercel)

## Custom Domain (Optional)

To add a custom domain:
1. Go to your Vercel project
2. Navigate to Settings → Domains
3. Add your domain
4. Follow DNS configuration instructions

## Monitoring

- View logs: Vercel Dashboard → Your Project → Logs
- Monitor performance: Vercel Dashboard → Your Project → Analytics
- Check errors: Vercel Dashboard → Your Project → Runtime Logs

## Security Checklist

✅ Environment variables are not committed to GitHub  
✅ `.env.local` is in `.gitignore`  
✅ Database uses SSL/TLS connection  
✅ Passwords are hashed with bcrypt  
✅ Sessions are encrypted with iron-session  
✅ HTTPS is enforced (automatic on Vercel)

## Support

If you encounter issues:
1. Check Vercel build logs
2. Verify environment variables
3. Test database connection
4. Review the README.md for setup instructions

---

Built with ❤️ by Dishant | Deployed on Vercel
