local FIREBASE_URL = "YOUR HOST"

local TeleportService = game:GetService("TeleportService")
local HttpService = game:GetService("HttpService")
local Workspace = game:GetService("Workspace")
local UserInputService = game:GetService("UserInputService")
local CoreGui = (gethui and gethui()) or game:GetService("CoreGui")
local Player = game:GetService("Players").LocalPlayer

local HopGuiName = "MobyServerHopGui"

-- Pulizia vecchie GUI
for _, v in pairs(CoreGui:GetChildren()) do
    if v.Name == HopGuiName or v.Name == "BestPetESP" then v:Destroy() end
end

local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = HopGuiName
ScreenGui.Parent = CoreGui
ScreenGui.ResetOnSpawn = false

local HopGui = Instance.new("Frame", ScreenGui)
HopGui.BackgroundColor3 = Color3.fromRGB(12, 12, 12)
HopGui.Position = UDim2.new(0.8, -250, 0.5, -150)
HopGui.Size = UDim2.new(0, 220, 0, 220)
HopGui.Active = true
Instance.new("UICorner", HopGui).CornerRadius = UDim.new(0, 8)
Instance.new("UIStroke", HopGui).Color = Color3.fromRGB(30, 30, 30)

local HopTitle = Instance.new("TextLabel", HopGui)
HopTitle.BackgroundTransparency = 1
HopTitle.Size = UDim2.new(1, 0, 0, 40)
HopTitle.Font = Enum.Font.GothamBold
HopTitle.Text = "Bot Server Hop & ESP"
HopTitle.TextColor3 = Color3.fromRGB(255, 255, 255)
HopTitle.TextSize = 14

local IsHopping = false
local AutoExecEnabled = false

local hopBtn = Instance.new("TextButton", HopGui)
hopBtn.Text = "START SERVER HOP"
hopBtn.Position = UDim2.new(0,15,0,50)
hopBtn.Size = UDim2.new(1,-30,0,35)
hopBtn.BackgroundColor3 = Color3.fromRGB(0, 106, 255)
hopBtn.TextColor3 = Color3.fromRGB(255,255,255)
hopBtn.Font = Enum.Font.GothamBold
Instance.new("UICorner", hopBtn).CornerRadius = UDim.new(0,6)

local espBtn = Instance.new("TextButton", HopGui)
espBtn.Text = "ESP BRAINROT [OFF]"
espBtn.Position = UDim2.new(0,15,0,95)
espBtn.Size = UDim2.new(1,-30,0,35)
espBtn.BackgroundColor3 = Color3.fromRGB(50, 180, 50)
espBtn.TextColor3 = Color3.fromRGB(255,255,255)
espBtn.Font = Enum.Font.GothamBold
Instance.new("UICorner", espBtn).CornerRadius = UDim.new(0,6)

local execBtn = Instance.new("TextButton", HopGui)
execBtn.Text = "AUTO EXECUTE [OFF]"
execBtn.Position = UDim2.new(0,15,0,140)
execBtn.Size = UDim2.new(1,-30,0,35)
execBtn.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
execBtn.TextColor3 = Color3.fromRGB(200, 200, 200)
execBtn.Font = Enum.Font.GothamBold
Instance.new("UICorner", execBtn).CornerRadius = UDim.new(0,6)

local fixLbl = Instance.new("TextLabel", HopGui)
fixLbl.Text = "AUTO FIX: ACTIVE"
fixLbl.Position = UDim2.new(0,15,0,185)
fixLbl.Size = UDim2.new(1,-30,0,25)
fixLbl.BackgroundTransparency = 1
fixLbl.TextColor3 = Color3.fromRGB(0, 255, 100)
fixLbl.Font = Enum.Font.GothamBold
fixLbl.TextSize = 12

-- Auto Fix Sempre Attivo
task.spawn(function()
    while task.wait(2) do
        if not Workspace:FindFirstChild("Debris") then
            local d = Instance.new("Folder")
            d.Name = "Debris"
            d.Parent = Workspace
        end
    end
end)

hopBtn.MouseButton1Click:Connect(function()
    if IsHopping then return end
    IsHopping = true
    hopBtn.Text = "HOPPING..."
    hopBtn.BackgroundColor3 = Color3.fromRGB(200, 150, 0)
    
    task.spawn(function()
        local placeId = game.PlaceId
        local function doHop()
            local servers = {}
            local req = game:HttpGet("https://games.roblox.com/v1/games/"..placeId.."/servers/Public?sortOrder=Asc&limit=100")
            if req then
                local data = HttpService:JSONDecode(req)
                if data and data.data then
                    for _, v in ipairs(data.data) do
                        if type(v) == "table" and v.playing < v.maxPlayers and v.id ~= game.JobId then
                            table.insert(servers, v.id)
                        end
                    end
                end
            end
            if #servers > 0 then
                local target = servers[math.random(1, #servers)]
                if AutoExecEnabled and queue_on_teleport then
                    pcall(function() queue_on_teleport("loadstring(game:HttpGet('YOUR_SCRIPT_HERE'))()") end)
                end
                TeleportService:TeleportToPlaceInstance(placeId, target, Player)
            end
        end
        while IsHopping do
            pcall(doHop)
            task.wait(1.5)
        end
    end)
end)

execBtn.MouseButton1Click:Connect(function()
    AutoExecEnabled = not AutoExecEnabled
    if AutoExecEnabled then
        execBtn.Text = "AUTO EXECUTE [ON]"
        execBtn.BackgroundColor3 = Color3.fromRGB(0, 150, 0)
    else
        execBtn.Text = "AUTO EXECUTE [OFF]"
        execBtn.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    end
end)

-- Dragging GUI
local hDragging, hDragStart, hStartPos
HopGui.InputBegan:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        hDragging = true
        hDragStart = input.Position
        hStartPos = HopGui.Position
    end
end)
HopGui.InputChanged:Connect(function(input)
    if hDragging and input.UserInputType == Enum.UserInputType.MouseMovement then
        local delta = input.Position - hDragStart
        HopGui.Position = UDim2.new(hStartPos.X.Scale, hStartPos.X.Offset + delta.X, hStartPos.Y.Scale, hStartPos.Y.Offset + delta.Y)
    end
end)
UserInputService.InputEnded:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then hDragging = false end
end)

local function parseValue(text)
    local clean = tostring(text or ""):gsub("%s", ""):gsub("/s", "")
    local num, suffix = clean:match("([%d%.]+)([KkMmBbTt]?)")
    if not num then return 0 end
    num = tonumber(num) or 0
    local mults = {K=1e3, M=1e6, B=1e9, T=1e12}
    return num * (mults[(suffix or ""):upper()] or 1)
end

getgenv().BestPetESP = getgenv().BestPetESP or { active = false, loop = nil }
local SentToFirebase = {}
local ActiveESPs = {} -- Evita il memory leak tracciando le parti con l'ESP
local httpRequest = (syn and syn.request) or (http and http.request) or request

local function sendToFirebase(name, valText, numVal)
    if not httpRequest then return end
    task.spawn(function() -- Usa task.spawn per evitare blocchi (freeze)
        local payload = {
            name = name,
            value = valText,
            numValue = numVal,
            jobId = game.JobId,
            placeId = game.PlaceId
        }
        local jsonData = HttpService:JSONEncode(payload)
        pcall(function()
            httpRequest({
                Url = FIREBASE_URL,
                Method = "POST",
                Body = jsonData,
                Headers = {["Content-Type"] = "application/json"}
            })
        end)
    end)
end

local function createESP(part, name, value)
    local bb = Instance.new("BillboardGui")
    bb.Name = "BestPetESP"
    bb.Size = UDim2.new(0, 200, 0, 50)
    bb.AlwaysOnTop = true
    bb.StudsOffset = Vector3.new(0, 3, 0)
    bb.Adornee = part
    bb.Parent = CoreGui
    
    local n = Instance.new("TextLabel", bb)
    n.Size = UDim2.new(1,0,0.5,0)
    n.BackgroundTransparency = 1
    n.Text = name
    n.TextColor3 = Color3.fromRGB(0, 150, 255)
    n.Font = Enum.Font.GothamBold
    n.TextScaled = true
    
    local v = Instance.new("TextLabel", bb)
    v.Size = UDim2.new(1,0,0.5,0)
    v.Position = UDim2.new(0,0,0.5,0)
    v.BackgroundTransparency = 1
    v.Text = value
    v.TextColor3 = Color3.fromRGB(255, 255, 255)
    v.Font = Enum.Font.GothamBold
    v.TextScaled = true

    return bb
end

local function startESP()
    if getgenv().BestPetESP.active then return end
    getgenv().BestPetESP.active = true
    
    getgenv().BestPetESP.loop = task.spawn(function()
        while getgenv().BestPetESP.active do
            local debris = Workspace:FindFirstChild("Debris")
            if debris then
                for _, template in ipairs(debris:GetChildren()) do
                    if template.Name == "FastOverheadTemplate" then
                        local sg = template:FindFirstChildOfClass("SurfaceGui")
                        if sg then
                            local gen = sg:FindFirstChild("Generation", true)
                            if gen and gen:IsA("TextLabel") and gen.Text ~= "" then
                                local valText = gen.Text
                                local numVal = parseValue(valText)
                                
                                if numVal >= 10000000 then -- Mostra e invia solo dai 10 Milioni in su
                                    local display = sg:FindFirstChild("DisplayName", true)
                                    local name = display and display.Text or "Brainrot"
                                    local part = sg.Adornee

                                    if part and part:IsA("BasePart") then
                                        -- Sistema Anti-Crash: Registra un ID unico per questo server, cosÃ¬ non lo re-invia mille volte
                                        local uniqueID = name .. "_" .. valText

                                        if not SentToFirebase[uniqueID] then
                                            SentToFirebase[uniqueID] = true
                                            sendToFirebase(name, valText, numVal)
                                        end
                                        
                                        -- Sistema Anti-Leak: Se la parte non ha un ESP associato in memoria, lo crea
                                        if not ActiveESPs[part] then
                                            ActiveESPs[part] = createESP(part, name, valText)
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
            end

            -- Pulizia Memory Leak: Rimuove l'ESP se la parte Ã¨ stata distrutta
            for part, bb in pairs(ActiveESPs) do
                if not part or not part.Parent then
                    if bb then bb:Destroy() end
                    ActiveESPs[part] = nil
                end
            end

            task.wait(1)
        end
    end)
end

espBtn.MouseButton1Click:Connect(function()
    if getgenv().BestPetESP.active then
        getgenv().BestPetESP.active = false
        if getgenv().BestPetESP.loop then task.cancel(getgenv().BestPetESP.loop) end
        
        -- Distrugge tutto
        for part, bb in pairs(ActiveESPs) do
            if bb then bb:Destroy() end
        end
        table.clear(ActiveESPs)

        for _, v in pairs(CoreGui:GetChildren()) do
            if v.Name == "BestPetESP" then v:Destroy() end
        end

        espBtn.Text = "ESP BRAINROT [OFF]"
        espBtn.BackgroundColor3 = Color3.fromRGB(50, 180, 50)
    else
        startESP()
        espBtn.Text = "ESP BRAINROT [ON]"
        espBtn.BackgroundColor3 = Color3.fromRGB(180, 50, 50)
    end
end)

