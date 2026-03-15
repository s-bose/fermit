# 2026-03-14 17:56:52

## Progress Report

We need to focus on RBAC first. ABAC is application-code layer enforcement. ReBAC can be implemented as a separate standalone API.

## RBAC

### Core Concepts

- Resource - Resource is a primary object that we control access to.
- Action - Specific actions to be performed on a resource. Actions are always bound to a specific resource type.
- Role - A role is a collection of permissions.

For Roles, there are two schools of thought:

1. We define roles as standalone collections of permissions and we implicitly aggregate all permissions from all related resources.

2. We define roles as part of resource. The role names are
