"""Wrapper to run the crypto trader with proper output flushing."""
import sys
import os

# Force unbuffered output
os.environ['PYTHONUNBUFFERED'] = '1'
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.crypto_trader import main
main()
