# 🔐 Password ManagerThis is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).



A secure, modern password manager built with Next.js 16, TypeScript, and PostgreSQL. Features a beautiful gradient UI with glassmorphism effects.## Getting Started



## ✨ FeaturesFirst, run the development server:



- 🔒 **Secure Authentication** - User registration and login with bcrypt password hashing```bash

- 🔑 **Password Vault** - Store and manage unlimited credentialsnpm run dev

- 👁️ **Show/Hide Passwords** - Toggle password visibility# or

- 📋 **Copy to Clipboard** - One-click password copyingyarn dev

- 🎲 **Password Generator** - Generate strong random passwords# or

- 🎨 **Beautiful UI** - Modern gradient design with glassmorphismpnpm dev

- 🔐 **Session Management** - Secure session handling with iron-session# or

- 💾 **PostgreSQL Database** - Production-ready Neon PostgreSQL databasebun dev

```

## 🚀 Tech Stack

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

- **Framework:** Next.js 16.0.5 (App Router)

- **Language:** TypeScriptYou can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

- **Styling:** Tailwind CSS 4

- **Database:** PostgreSQL (Neon)This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

- **Authentication:** iron-session + bcrypt

- **Deployment:** Vercel## Learn More



## 📦 InstallationTo learn more about Next.js, take a look at the following resources:



1. Clone the repository:- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.

```bash- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

git clone https://github.com/Dishant707/MachineLearning_Algorithms_Dishant-.git

cd MachineLearning_Algorithms_Dishant-/email-password-managerYou can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

```

## Deploy on Vercel

2. Install dependencies:

```bashThe easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

npm install

```Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.


3. Set up environment variables:
Create a `.env.local` file in the root directory:
```env
SECRET_COOKIE_PASSWORD="your-secret-cookie-password-min-32-chars"
DATABASE_URL="your-neon-postgresql-connection-string"
```

4. Set up the database:
```bash
npm run db:setup
```

5. Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the app.

## 🌐 Deploy to Vercel

### Prerequisites
- A [Vercel account](https://vercel.com)
- A [Neon PostgreSQL database](https://neon.tech)

### Deployment Steps

1. **Push your code to GitHub**
```bash
cd /path/to/MachineLearning_Algorithms_Dishant-
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Import to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/new)
   - Click "Import Project"
   - Import your GitHub repository: `Dishant707/MachineLearning_Algorithms_Dishant-`
   - **Important:** Set Root Directory to `email-password-manager`

3. **Configure Environment Variables in Vercel**
   Add these in Project Settings → Environment Variables:
   ```
   SECRET_COOKIE_PASSWORD=your-strong-secret-min-32-characters
   DATABASE_URL=postgresql://neondb_owner:password@host.neon.tech/neondb?sslmode=require
   ```

4. **Deploy**
   - Click "Deploy"
   - Vercel will automatically build and deploy your app
   - Your app will be live at `https://your-project.vercel.app`

## 🗂️ Project Structure

```
email-password-manager/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth/          # Authentication endpoints
│   │   │   └── credentials/   # Credential management
│   │   ├── login/             # Login page
│   │   ├── register/          # Registration page
│   │   └── page.tsx           # Dashboard (protected)
│   ├── components/
│   │   └── Dashboard.tsx      # Main password vault component
│   └── lib/
│       ├── db.ts              # Database connection
│       └── session.ts         # Session management
├── scripts/
│   └── setup-db.ts            # Database setup script
└── public/                    # Static assets
```

## 🔒 Security Features

- Password hashing with bcrypt (10 rounds)
- Secure session management with iron-session
- HTTPS required in production
- SQL injection protection with parameterized queries
- Environment variables for sensitive data
- SSL/TLS database connections

## 📝 API Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/logout` - Logout user
- `GET /api/credentials` - Get all user credentials
- `POST /api/credentials` - Add new credential
- `DELETE /api/credentials/[id]` - Delete credential

## 🎨 UI Features

- Beautiful purple-blue gradient background
- Glassmorphism card designs
- Smooth animations and transitions
- Responsive design for all devices
- Icon-based navigation
- Visual feedback for user actions
- Password visibility toggle
- One-click copy to clipboard

## 👨‍💻 Author

**Dishant**
- GitHub: [@Dishant707](https://github.com/Dishant707)
- Repository: [MachineLearning_Algorithms_Dishant-](https://github.com/Dishant707/MachineLearning_Algorithms_Dishant-)

## 📄 License

This project is open source and available under the MIT License.

---

Built with ❤️ using Next.js and deployed on Vercel
