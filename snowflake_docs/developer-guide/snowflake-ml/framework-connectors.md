# Snowpark ML Framework Connectors¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) [Preview
Feature](../../release-notes/preview-features) — Open

Available to all accounts.

Snowpark ML includes support for secure, scalable data provisioning for the
PyTorch and Tensorflow frameworks, both of which expect data in their own
specific formats. To simplify this workflow, the Snowpark ML library provides
convenient methods built on top of the FileSet API to provide data from a
FileSet as PyTorch Tensors or TensorFlow Records. (A [FileSet](filesystem-
fileset.html#label-snowpark-ml-fileset) represents an immutable snapshot of
the result of a SQL query in the form of files in an internal server-side
encrypted stage.)

Note

This topic assumes that the Snowpark ML module is installed. If it isn’t, see
[Using Snowflake ML Locally](snowpark-ml.html#label-snowpark-ml-get-started).

## Creating a FileSet from a Query¶

Refer to [Creating and Using a FileSet](filesystem-fileset.html#label-
snowpark-ml-fileset) for information on creating a FileSet from the data you
want to use with PyTorch or TensorFlow. Then continue to one of the following
sections:

  * Feeding a FileSet to PyTorch

  * Feeding a FileSet to TensorFlow

## Feeding a FileSet to PyTorch¶

From a Snowflake FileSet, you can get a PyTorch DataPipe, which can be passed
to a PyTorch DataLoader. The DataLoader iterates over the FileSet data and
yields batched PyTorch tensors. Create the DataPipe using the FileSet’s
`to_torch_datapipe` method, and then pass the DataPipe to PyTorch’s
`DataLoader`:

    
    
    from torch.utils.data import DataLoader
    
    # See later sections about shuffling and batching
    pipe = fileset_df.to_torch_datapipe(
        batch_size=4,
        shuffle=True,
        drop_last_batch=True)
    
    for batch in DataLoader(pipe, batch_size=None, num_workers=0):
        print(batch)
        break
    

Copy

## Feeding a FileSet to TensorFlow¶

You can get a TensorFlow Dataset from a Snowflake FileSet using the FileSet’s
`to_tf_dataset` method:

    
    
    import tensorflow as tf
    
    # See following sections about shuffling and batching
    ds = fileset_df.to_tf_dataset(
        batch_size=4,
        shuffle=True,
        drop_last_batch=True)
    
    for batch in ds:
        print(batch)
        break
    

Copy

Iterating over the Dataset yields batched tensors.

## Shuffling Data in FileSets¶

It is often valuable to shuffle the training data to avoid overfitting and
other issues. For a discussion of the value of shuffling, see [Why should the
data be shuffled for machine learning
tasks?](https://datascience.stackexchange.com/questions/24511/why-should-the-
data-be-shuffled-for-machine-learning-tasks)

If your query does not already shuffle your data sufficiently, a FileSet can
shuffle data at two points:

  * When the FileSet is created by using `FileSet.make`.

All rows in your query are shuffled before they are written to the FileSet.
This is a high-quality global shuffle and can be expensive with large
datasets. Therefore, it is performed only once, when materializing the
FileSet. Pass `shuffle=True` as a keyword argument to `FileSet.make`.

  * When you create a PyTorch DataPipe or a TensorFlow Dataset from a FileSet.

At this point, the order of the files in the FileSet is randomized, as is the
order of the rows in each file. This can be considered an “approximate” global
shuffle. It is of lower quality than a true global shuffle, but it is much
less expensive. To shuffle at this stage, pass `shuffle=True` as a keyword
argument to the FileSet’s `to_torch_datapipe` or `to_tf_dataset` method.

For best results, shuffle twice: when creating the FileSet and when feeding
the data to PyTorch or TensorFlow.

## Batching Data in FileSets¶

FileSets have a batching feature that works the same as the batching
functionality in PyTorch and TensorFlow but is more efficient. Snowflake
recommends that you use the `batch_size` parameter in the FileSet’s
`to_torch_datapipe` and `to_tf_dataset` methods instead of having PyTorch or
TensorFlow do the batching. With PyTorch, to disable its batching
functionality, you must explicitly pass `batch_size=None` when instantiating
`DataLoader`.

You can also drop the last batch if it is incomplete by passing
`drop_last_batch=True` to `to_torch_datapipe` or to `to_tf_dataset`.

