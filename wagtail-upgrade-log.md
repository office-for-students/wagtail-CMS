# Wagtail Upgrade

## Purpose

This document serves the purpose of keeping a log of additional commands run while
upgrading Wagtail from 2.15.5.

## 2.x

### 2.15.5 to 2.16.3

No additional commands required

## 3.x

### 2.16.3 to 3.0

`python manage.py migrate` - required for functionality

`python manage.py update_index` - re-indexes search and enables search functionality

### 3.0 to 3.0.3

No additional commands required

