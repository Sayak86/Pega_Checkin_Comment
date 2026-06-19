## Specific Instructions for Connect-REST

You are analysing changes to a **Connect-REST** rule. Use the sections below to decide what is worth reporting and how to phrase it. The generic instructions already told you how to read `pxChangeType`, `pxCurrentValue`, and `pxPreviousValue` — do not repeat that mechanic, just apply it.

Only report features that actually changed in the diff. Do not describe anything that did not change. Ignore metadata (history, UUIDs, timestamps, labels).

=====================================================================

## WHAT TO TRACK

### TAB 1 — Methods Tab

**Request Headers section**
1. Request header name changes for POST/GET/PUT/PATCH/DELETE (e.g. `.pyPOSTRequestHeaders(n).pyParameterName`).
2. Inserted or removed header rows (e.g. `.pyPOSTRequestHeaders(n)`, `.pyGETRequestHeaders(n)`).

**Query String Parameters section**
1. Request query parameter name changes for POST/GET/PUT/PATCH/DELETE (e.g. `.pyPOSTRequestParameters(n).pyParameterName`).
2. Inserted or removed parameter rows (e.g. `.pyPOSTRequestParameters(n)`, `.pyGETRequestParameters(n)`).

**Message Data section (Request body mapping)**
1. Map-from source type changes — JSON, XML, Clipboard, Constant, or HTML Stream (e.g. `.pyPOSTRequestDataList(n).pyMapFrom`).
2. Map-from key changes — the clipboard page/property used as source (e.g. `.pyPOSTRequestDataList(n).pyMapFromKey`).
3. Fast JSON processing flag toggle (e.g. `.pyPOSTRequestDataList(n)`).
4. DatalistDescription field additions/changes (e.g. `.pyPOSTRequestDataList(n).pyDesc`).

### TAB 2 — Service Tab

**Resource properties section**
1. Resource path changes (e.g. `.pyResourcePath`).
2. Resource parameter additions/removals (e.g. `.pyResourceParameters(n)`).

**Integration System section**
1. Integration system ID additions/changes (e.g. `.pyIntegrationSystemId`).

**Connection section**
1. Response timeout value changes (e.g. `.pyResponseTimeout`).

**Processing Options section**
1. Request processor additions/changes (e.g. `.pyRequestProcessor`).

**Error Handling section**
1. Handler flow changes (e.g. `.pyHandlerFlow`).
2. Status value property changes (e.g. `.pyStatusValProperty`).
3. Status message property changes (e.g. `.pyStatusMsgProperty`).
4. Response data fast JSON processing flag (e.g. `.pyPOSTResponseDataList(n).pyUseFastJSONProcessing`).

**Security Settings section**
1. Keystore name additions/changes (e.g. `.pyKeystoreName`).
2. Truststore name additions/changes (e.g. `.pyTruststoreName`).

=====================================================================

## HOW TO PHRASE CHANGES (verb rules — mandatory)

**Booleans**
- `pxCurrentValue == "true"`  → Enabled `<feature>`.
- `pxCurrentValue == "false"` → Disabled `<feature>`.

**Strings / scalars**
- Always use the order: Updated `<feature>` to `'<new_value>'` from `'<old_value>'`.
- `pxPreviousValue` is always `<old_value>`; `pxCurrentValue` is always `<new_value>`.
- Empty previous → non-empty current → Set `<feature>` to `'<new_value>'`.
- Non-empty previous → empty current → Cleared `<feature>`.

**Structural nodes with no scalar value (inserted)**
- Inserted row with no value (e.g. `.pyPOSTRequestHeaders(3)`) → Added POST request header 3.
- Removed row → Removed `<feature>`.

**Headers / params / rows (mention each individually, do NOT generalise)**
- Modified `.pyPOSTRequestHeaders(n).pyParameterName` → Updated POST request header `<n>` name to `'<new_value>'` from `'<old_value>'`.
- Inserted `.pyPOSTRequestHeaders(n)` → Added POST request header `<n>`.
- The same rules apply to GET, PUT, PATCH, DELETE headers, parameters, and resource parameters.

**Order rule (mandatory)**
- Always write `to` before `from` in every change description.
- CORRECT:   Updated handler flow to `'<new_flow>'` from `'<old_flow>'`.
- INCORRECT: Updated handler flow from `'<old_flow>'` to `'<new_flow>'`.

=====================================================================

## EXAMPLES (tab-wise)

**Service Tab** — keep all Service-tab changes together and start the sentence with "In services tab":
1. Increased response timeout to `'<new_timeout>'` from `'<old_timeout>'` ms in connection section.
2. Updated handler flow to `'<new_flow>'` from `'<old_flow>'`, updated status value property to `'<old_val>'` and updated status message property to `'<new_msg>'` from `'<old_msg>'` in error handling section.
3. Enabled fast JSON processing for POST response data 1 in error handling section.
4. Set request processor to `'<processor_name>'` in processing options section.
5. Set keystore to `'<keystore_name>'` and truststore to `'<truststore_name>'` in security settings section.
6. Set integration system ID to `'<integration_system_id>'` in integration system section.

**Methods Tab** — keep all Methods-tab changes together and start the sentence with "In methods tab":
1. Updated resource path to `'<new_resource_path>'` from `'<old_resource_path>'` and added resource parameter `<n>` in resource properties section.
2. Updated POST request header 1 name to `'<new_header_1>'` from `'<old_header_1>'`, updated POST request header 2 name to `'<new_header_2>'` from `'<old_header_2>'` and added POST request header `<n>` in request headers section.
3. Updated POST request parameter 1 name to `'<new_param_1>'` from `'<old_param_1>'`, updated POST request parameter 2 name to `'<new_param_2>'` from `'<old_param_2>'` and added POST request parameter `<n>` in query string parameters section.
4. Updated POST request data 1 map-from source to `'<new_map_from>'` from `'<old_map_from>'`, updated map-from key to `'<new_map_key>'` from `'<old_map_key>'`, enabled fast JSON processing for POST request data 1 and set description to `'<description>'` in message data section.
5. Disabled fast JSON processing for PUT request data 1, GET response data 1 and PATCH request data 1 in message data section.
6. Updated POST response data 1 map-to target to `'<new_map_to>'` from `'<old_map_to>'` and updated map-to key to `'<new_map_to_key>'` from `'<old_map_to_key>'` in message data section.

=====================================================================

## CONSTRAINTS

- You may use the property references from the JSON to understand what changed, but focus only on changed features. Do not add anything that did not change in the diff.
- You must mention the exact change for every updated, modified, or inserted field.
- Do not mention anything unrelated to actual REST connector logic, mappings, parameters, or referenced properties as described above.
- Do not use semicolons — use commas only.
- Do not use backslashes anywhere in the output.
- Do not use raw Pega property references in the output — always use the human-friendly label defined above.
- Always wrap property values and names in single quotes like `'value'`.
- Always write `to` before `from` — never reverse this order.

## OUTPUT

Compose one concise, business-friendly commit sentence in past tense covering all changes across both tabs.
