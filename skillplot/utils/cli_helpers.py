import random

def random_partition(input_list, num_partitions):
    # random.shuffle(input_list)  # Shuffle the input list randomly
    partitions = []
    partition_size = len(input_list) // num_partitions
    
    for _ in range(num_partitions):
        # Create a partition by slicing the shuffled input list
        partition = input_list[:partition_size]
        partitions.append(partition)
        
        # Remove the elements of the partition from the input list
        input_list = input_list[partition_size:]
    
    # Append remaining elements to the last partition
    partitions[-1].extend(input_list)
    # # Distribute any remaining elements
    # for i, element in enumerate(input_list):
    #     partitions[i % num_partitions].append(element)
    
    return partitions