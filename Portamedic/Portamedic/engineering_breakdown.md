# Portamedic Engineering Task Breakdown

**Last Updated:** December 16, 2025  
**Status:** Draft for Cori Review

---

## Endpoint Status Check (Completed)

| Endpoint | URL | Status |
|----------|-----|--------|
| Auth Token | `https://auth.integratedtestingservices.com:8020/TokenService/connect/token` | ✅ Reachable (400 without creds) |
| NewCaseSubmit | `https://www.integratedtestingservices.com/clinical/NewCaseSubmit` | ✅ Reachable (401 without auth) |
| Schedule4Real SOAP | `https://www.integratedtestingservices.com/S4R/mainservice.asmx` | ✅ WSDL accessible |

**Conclusion:** All Portamedic sandbox endpoints are live and responding correctly. Blocked on credentials.

---

## Phase 1 Deliverables

### Deliverable 1: Unscheduled Appointment Path (Preferred Time Flow)
*Timeline per schedule: 1/12/2026 - 2/2/2026 (15 business days)*

This is the **existing integration** approach (same as Natera). We send a preferred date/time, Portamedic schedules via Traditional Scheduling.

| Task | Description | Est. | Blocked On |
|------|-------------|------|------------|
| 1.1 | Re-enable Portamedic feature flags (Kodama disabled) | 2h | Kodama availability |
| 1.2 | Verify sandbox credentials work with token service | 1h | **Credentials from Portamedic** |
| 1.3 | Test CheckAvailability SOAP call in sandbox | 2h | 1.2 |
| 1.4 | Test MakeReservation SOAP call in sandbox | 2h | 1.3 |
| 1.5 | Test NewCaseSubmit REST call in sandbox | 2h | 1.2 |
| 1.6 | Configure new study (Walgreens) in Trial Builder | 2h | Account Number from Portamedic |
| 1.7 | End-to-end test: participant → availability → book → order | 4h | 1.1-1.6 |
| 1.8 | Document configuration steps for CSM | 2h | 1.7 |

**Subtotal: ~17 hours (2-3 days)**

---

### Deliverable 2: Status Retrieval via Webhook (NEW)
*Timeline per schedule: 1/30/2026 - 3/11/2026 (28 business days)*

This is **new work** based on v2 API documentation. Portamedic will POST status updates to our webhook.

| Task | Description | Est. | Blocked On |
|------|-------------|------|------------|
| 2.1 | Design webhook endpoint architecture | 4h | - |
| 2.2 | Create webhook receiver endpoint in Integrations API | 8h | 2.1 |
| 2.3 | Implement webhook authentication (Bearer or OAuth2) | 4h | Decision from Portamedic |
| 2.4 | Parse ClinicalCase JSON status payload | 4h | 2.2 |
| 2.5 | Map Portamedic status codes to Curebase statuses | 4h | Product decision on mapping |
| 2.6 | Update participant/visit booking status in DB | 8h | 2.4, 2.5 |
| 2.7 | Surface status updates in WebApp UI | 8h | 2.6 |
| 2.8 | Handle event codes (INFO, CONTACT, SCHEDULED, IMAGED) | 4h | 2.4 |
| 2.9 | (Optional) Handle image attachments (PDF base64) | 8h | Product decision |
| 2.10 | Create webhook URL for Portamedic (infra/DevOps) | 2h | - |
| 2.11 | Provide webhook credentials to Portamedic | 1h | 2.10 |
| 2.12 | End-to-end test with Portamedic sandbox | 8h | 2.1-2.11 |
| 2.13 | Document webhook integration | 2h | 2.12 |

**Subtotal: ~65 hours (8-10 days)**

---

### Deliverable 3: Re-enable Portamedic Integrations (Kodama)
*Prerequisite for all other work*

| Task | Description | Est. | Blocked On |
|------|-------------|------|------------|
| 3.1 | Identify what was disabled and why | 2h | Kodama |
| 3.2 | Fix erroneous logging issues that caused disabling | 4h | 3.1 |
| 3.3 | Re-enable feature flags | 1h | 3.2 |
| 3.4 | Verify no regressions on existing integrations | 4h | 3.3 |

**Subtotal: ~11 hours (1-2 days)**

---

## Summary

| Deliverable | Estimated Hours | Business Days | Dependencies |
|-------------|-----------------|---------------|--------------|
| 1. Unscheduled Appointment Path | 17h | 2-3 days | Credentials, Account # |
| 2. Status Retrieval Webhook | 65h | 8-10 days | Product decisions, Infra |
| 3. Re-enable Integration | 11h | 1-2 days | Kodama availability |
| **Buffer (20%)** | ~19h | 2-3 days | - |
| **TOTAL** | ~112h | **14-18 days** | - |

---

## Blockers (Need from Cori/Walgreens/Portamedic)

### Critical (Blocks all work)
- [ ] **Sandbox ClientID** - from Portamedic
- [ ] **Sandbox Client Secret** - from Portamedic
- [ ] **Account Number** - from Portamedic/Walgreens

### Required for Status Webhook
- [ ] **Webhook authentication preference** - Bearer token or OAuth2?
- [ ] **Do we need image attachments?** - or just status codes
- [ ] **Status mapping** - which Portamedic statuses map to which Curebase states?

### Internal
- [ ] **Kodama** - what was disabled and scope of fix
- [ ] **DevOps** - webhook URL provisioning

---

## Questions for Cori

1. **When can we expect sandbox credentials?** This blocks all validation work.

2. **For status webhook - what URL format do we want?**
   - Option A: `https://integrations.curebase.com/portamedic/webhook`
   - Option B: Study-specific: `https://integrations.curebase.com/webhook/{studyId}/portamedic`

3. **Which statuses do we actually need to track?**
   - ENTERED (order received)
   - READY_FOR_APPOINTMENT (can be scheduled)
   - SCHEDULED (appointment confirmed)
   - SERVICES_COMPLETE (visit done)
   - COMPLETED (case closed)
   - CANCELLED

4. **Do we need PDF attachments?** v2 docs show Portamedic can send completed case images. Do we need to store/display these?

5. **Is the 28 business days for status retrieval realistic?** Based on breakdown it's ~65 hours of work.

---

## Timeline Fit

Per the project timeline:
- **Build preferred time flow:** 1/12/2026 - 2/2/2026 ✅ Fits (17h = 2-3 days)
- **Pull back statuses (eng):** 1/30/2026 - 3/11/2026 ✅ Fits (65h = 8-10 days, 28 days allocated)
- **Internal Testing:** 2/17/2026 - 2/25/2026
- **UAT:** 3/2/2026 - 3/6/2026

**Risk:** If credentials arrive late, we compress testing time.

