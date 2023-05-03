# Control Flow
```mermaid

sequenceDiagram
    actor U as User
    participant L as LinkShell
    participant Delay as DelayShell
    participant Loss as LossShell
    U ->> Delay:  mm-delay delay-milliseconds [command...]
    U ->> L: mm-link

```

# DelayShell

```mermaid
sequenceDiagram
    participant Delay as DelayShell
    participant PacketShell as PacketShell<DelayQueue>
    Delay ->> PacketShell: starts up_link
    Delay ->> PacketShell: starts down_link

```

# LinkShell

```mermaid
sequenceDiagram
    actor U as User
    participant LinkShell as LinkShell
    participant PacketShell as PacketShell<LinkQueue>
    U ->> LinkShell: specifies queueing type
    activate LinkShell
    LinkShell ->> U: InfinitePacketQueue or Droptail or Drophead or Codel or Pie
    LinkShell ->> PacketShell: starts up_link
    LinkShell ->> PacketShell: starts down_link


```
- required argument: `uplink-log, downlink-log, uplink-queue, downlink-queue, uplink-queue-args, downlink-queue-args`
- no argument: `once, meter-uplink, meter-downlink, meter-uplink-delay, meter-downlink-delay, meter-all`
