# 🌱 Carbon Footprint Tracker API

A production-ready REST API that helps small businesses track, analyze, and reduce their carbon emissions. Businesses can log daily activities like electricity usage, fuel consumption, shipping, and waste — and get real-time CO₂ calculations, monthly analytics, and actionable reduction suggestions.

---

## 🚀 Live Demo

> _Will be added after deployment on Day 10_

## 📖 API Documentation (Swagger)

> _Will be added after Day 9_

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Runtime | Node.js |
| Framework | Express.js |
| Database | PostgreSQL 15 |
| ORM | Prisma 7 |
| Caching | Redis |
| Queue / Jobs | Bull |
| Auth | JWT (JSON Web Tokens) |
| Email | Nodemailer |
| Docs | Swagger / OpenAPI |
| Containerization | Docker + docker-compose |
| Deployment | Railway |

---

## 📁 Project Structure

```
carbon-footprint-tracker/
├── src/
│   ├── controllers/       # Handles request/response logic
│   ├── routes/            # Defines API endpoints
│   ├── middleware/        # Auth checks, error handling
│   ├── services/          # Business logic & CO₂ calculations
│   ├── utils/             # Helper functions
│   ├── config/            # DB, Redis config
│   ├── queues/            # Bull background jobs
│   ├── app.js             # Express app setup
│   └── server.js          # Server entry point
├── prisma/
│   ├── schema.prisma      # Database schema
│   └── migrations/        # Migration history
├── .env.example           # Environment variable template
├── prisma.config.js       # Prisma 7 configuration
├── docker-compose.yml     # Docker setup (Day 10)
└── package.json
```

---

## 🗄️ Database Schema

```
User
 └── Business
      └── ActivityLog ──── ActivityCategory
                                └── EmissionFactor
```

- **User** — stores login credentials
- **Business** — company profile linked to a user
- **ActivityCategory** — categories like Electricity, Fuel, Shipping, Waste
- **EmissionFactor** — CO₂ multiplier per unit for each category
- **ActivityLog** — individual activity entries with auto-calculated CO₂

---

## ⚙️ Local Setup

### Prerequisites

- Node.js v18+
- PostgreSQL 15
- Redis
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/developer7620/carbon-footprint-tracker.git
cd carbon-footprint-tracker

# 2. Install dependencies
npm install

# 3. Create your .env file
cp .env.example .env
# Fill in your values in .env

# 4. Run database migrations
npx prisma migrate dev

# 5. Start the development server
npm run dev
```

### Environment Variables

Create a `.env` file in the root directory:

```env
PORT=3000
DATABASE_URL="postgresql://carbon_user:carbon123@localhost:5432/carbon_tracker"
JWT_SECRET="your_super_secret_jwt_key"
REDIS_URL="redis://localhost:6379"
```

---

## 📡 API Endpoints

> Full interactive documentation available via Swagger UI at `/api/docs`

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and get JWT token |

### Business
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/business` | Create business profile |
| GET | `/api/business` | Get business profile |
| PUT | `/api/business` | Update business profile |

### Activity Logs
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/logs` | Log a new activity |
| GET | `/api/logs` | Get all activity logs |
| DELETE | `/api/logs/:id` | Delete an activity log |

### Analytics
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/analytics/monthly` | Monthly CO₂ summary |
| GET | `/api/analytics/trends` | Historical trend data |
| GET | `/api/analytics/suggestions` | Reduction suggestions |

---

## 🧮 CO₂ Calculation Logic

Each activity log calculates emissions as:

```
CO₂ (kg) = Quantity × Emission Factor
```

### Default Emission Factors

| Category | Unit | Factor (kg CO₂ per unit) |
|---|---|---|
| Electricity | kWh | 0.82 |
| Fuel (Petrol) | Litre | 2.31 |
| Fuel (Diesel) | Litre | 2.68 |
| Shipping | km | 0.21 |
| Waste | kg | 0.45 |

---

## 🔐 Authentication

This API uses **JWT (JSON Web Tokens)**. After login, include the token in all protected requests:

```
Authorization: Bearer <your_token>
```

---

## 🧪 Testing the API

Import the Postman collection (coming soon) or use the Swagger UI at:

```
http://localhost:3000/api/docs
```

---

## 📦 Docker Setup

> _Coming on Day 10_

```bash
docker-compose up --build
```

---

## 🌍 Deployment

> _Deployed on Railway — link coming on Day 10_

---

## 📅 Build Journal

| Day | What was built |
|---|---|
| Day 1 | Project setup, folder structure, PostgreSQL, Prisma schema & migration |
| Day 2 | User authentication — register, login, JWT middleware _(coming soon)_ |
| Day 3 | Business profile APIs _(coming soon)_ |
| Day 4 | Activity categories + emission factors _(coming soon)_ |
| Day 5 | Activity logging with CO₂ calculation _(coming soon)_ |
| Day 6 | Analytics & reporting APIs _(coming soon)_ |
| Day 7 | Redis caching + Bull queue setup _(coming soon)_ |
| Day 8 | Background email reports _(coming soon)_ |
| Day 9 | Swagger docs + validation + error handling _(coming soon)_ |
| Day 10 | Docker + Railway deployment _(coming soon)_ |

---

## 👨‍💻 Author

**Aditya** — [@developer7620](https://github.com/developer7620)

---

## 📄 License

MIT License — feel free to use this project as a reference.
