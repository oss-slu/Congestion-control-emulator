#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <bcc/proto.h>
#include <linux/tcp.h>

struct data_t {
    u32 cwnd;
};

BPF_PERF_OUTPUT(events);

int trace_tcp_cong(struct pt_regs *ctx, struct sock *sk, struct tcp_sock *ts)
{
    struct data_t data = {};

    //if (ts->delivered > 0) {
    data.cwnd = ts->snd_cwnd;
    events.perf_submit(ctx, &data, sizeof(data));
    //}

    return 0;
}
