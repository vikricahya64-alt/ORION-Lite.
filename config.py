"""
==========================================
ORION Lite Configuration
==========================================
"""

# ========================================
# DEVICE PROFILE
# ========================================

PROFILE = "lite"

# ========================================
# RUNTIME
# ========================================

RUNTIME_INTERVAL = 5

IDLE_INTERVAL = 10

SLEEP_INTERVAL = 30

# ========================================
# BATTERY
# ========================================

BATTERY_WARNING = 30

BATTERY_CRITICAL = 15

# ========================================
# DATABASE
# ========================================

DATABASE_PATH = "logs/orion.db"

DATABASE_MAX_MB = 100

AUTO_OPTIMIZE = True

AUTO_CLEAN_MEMORY = True

AUTO_VACUUM = True

# ========================================
# MEMORY
# ========================================

MAX_PROGRESS_HISTORY = 100

MAX_MEMORY_PER_CATEGORY = 1000

REMOVE_DUPLICATE_MEMORY = True

AUTO_SUMMARY = True

# ========================================
# LOG
# ========================================

ENABLE_LOG = True

LOG_LEVEL = "INFO"

KEEP_LOG_DAYS = 7

# ========================================
# WORKER
# ========================================

MAX_JOB_PER_LOOP = 1

# ========================================
# PERFORMANCE
# ========================================

if PROFILE == "lite":

    RUNTIME_INTERVAL = 5

    MAX_JOB_PER_LOOP = 1

    MAX_MEMORY_PER_CATEGORY = 500

elif PROFILE == "balanced":

    RUNTIME_INTERVAL = 3

    MAX_JOB_PER_LOOP = 3

    MAX_MEMORY_PER_CATEGORY = 1500

elif PROFILE == "performance":

    RUNTIME_INTERVAL = 1

    MAX_JOB_PER_LOOP = 10

    MAX_MEMORY_PER_CATEGORY = 5000
