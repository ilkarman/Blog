# Custom data loader for MXNET

def load_data_frame(X_data, y_data, batch_size=128, shuffle=False):
    """
    For low RAM this methods allows us to keep only the original data
    in RAM and calculate the features (which are orders of magnitude bigger
    on the fly). This keeps only 10 batches worth of features in RAM using
    asynchronous programing and yields one DataBatch() at a time.
    """

    if shuffle:
        idx = X_data.index
        assert len(idx) == len(y_data)
        rnd = np.random.permutation(idx)
        X_data = X_data.reindex(rnd)
        y_data = y_data[rnd]

    # Dictionary to create character vectors
    character_hash = pd.DataFrame(np.identity(len(ALPHABET), dtype='bool'), columns=ALPHABET)

    # Yield processed batches asynchronously
    # Buffy 'batches' at a time
    def async_prefetch_wrp(iterable, buffy=30):
        poison_pill = object()

        def worker(q, it):
            for item in it:
                q.put(item)
            q.put(poison_pill)

        queue = Queue.Queue(buffy)
        it = iter(iterable)
        thread = threading.Thread(target=worker, args=(queue, it))
        thread.daemon = True
        thread.start()
        while True:
            item = queue.get()
            if item == poison_pill:
                return
            else:
                yield item

    # Async wrapper around
    def async_prefetch(func):
        @functools.wraps(func)
        def wrapper(*args, **kwds):
            return async_prefetch_wrp(func(*args, **kwds))
        return wrapper

    @async_prefetch
    def feature_extractor(dta, val):
        # Yield mini-batch amount of character vectors
        X_split = np.zeros([batch_size, 1, FEATURE_LEN, len(ALPHABET)], dtype='bool')
        for ti, tx in enumerate(dta):
            chars = list(tx)
            for ci, ch in enumerate(chars):
                if ch in ALPHABET:
                    X_split[ti % batch_size][0][ci] = np.array(character_hash[ch], dtype='bool')
            # No padding -> only complete batches processed
            if (ti + 1) % batch_size == 0:
                yield mx.nd.array(X_split), mx.nd.array(val[ti + 1 - batch_size:ti + 1])
                X_split = np.zeros([batch_size, 1, FEATURE_LEN, len(ALPHABET)], dtype='bool')

    # Yield one mini-batch at a time and asynchronously process to keep 4 in queue
    for Xsplit, ysplit in feature_extractor(X_data, y_data):
        yield DataBatch(data=[Xsplit], label=[ysplit])