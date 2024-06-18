
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'se_reads': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='activate when using single end reads input',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'skip_qc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Quality control options',
        description='Skip all QC steps except for MultiQC.',
    ),
    'skip_fastqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip FastQC.',
    ),
    'clip_r1': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='trimming options',
        description="Instructs Trim Galore to remove bp from the 5' end of read 1 (or single-end reads).",
    ),
    'clip_r2': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description="Instructs Trim Galore to remove bp from the 5' end of read 2 (paired-end reads only).",
    ),
    'three_prime_clip_r1': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description="Instructs Trim Galore to remove bp from the 3' end of read 1 AFTER adapter/quality trimming has been performed.",
    ),
    'three_prime_clip_r2': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description="Instructs Trim Galore to remove bp from the 3' end of read 2 AFTER adapter/quality trimming has been performed.",
    ),
    'save_trimmed': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save the trimmed FastQ files in the results directory.',
    ),
    'trim_nextseq': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Instructs Trim Galore to apply the --nextseq=X option, to trim based on quality after removing poly-G tails.',
    ),
    'skip_trimming': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip the adapter trimming step.',
    ),
    'sequence_filter': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Filtering options',
        description='Fasta file with sequences to filter away before running assembly etc..',
    ),
    'bbnorm': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Digital normalization options',
        description='Perform normalization to reduce sequencing depth.',
    ),
    'bbnorm_target': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title=None,
        description='Reduce the number of reads for assembly average coverage of this number.',
    ),
    'bbnorm_min': NextflowParameter(
        type=typing.Optional[int],
        default=5,
        section_title=None,
        description='Reads with an apparent depth of under nx will be presumed to be errors and discarded',
    ),
    'save_bbnorm_fastq': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='save the resulting fastq files from normalization',
    ),
    'assembler': NextflowParameter(
        type=typing.Optional[str],
        default='megahit',
        section_title='Assembler options',
        description='Specify which assembler you would like to run, possible alternatives: megahit, rnaspades. default: megahit',
    ),
    'assembly': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to a fasta file with a finished assembly. Assembly will be skipped by the pipeline.',
    ),
    'min_contig_length': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title=None,
        description='Filter out contigs shorter than this.',
    ),
    'save_bam': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Mapping options',
        description='Save the bam files from mapping',
    ),
    'save_samtools': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save the output from samtools',
    ),
    'protein_fasta': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Orf Caller options',
        description='Path to a protein fasta file',
    ),
    'gff': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to a gff file',
    ),
    'orf_caller': NextflowParameter(
        type=typing.Optional[str],
        default='prodigal',
        section_title=None,
        description='Specify which ORF caller you would like to run, possible alternatives: prodigal, prokka, transdecoder, default: prodigal.',
    ),
    'prodigal_trainingfile': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Specify a training file for prodigal. By default prodigal will learn from the input sequences',
    ),
    'skip_eggnog': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title='Functional annotation options',
        description='Skip EGGNOG functional annotation',
    ),
    'eggnog_dbpath': NextflowParameter(
        type=typing.Optional[str],
        default='eggnog',
        section_title=None,
        description='Specify EGGNOG database path',
    ),
    'skip_kofamscan': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title=None,
        description='skip kofamscan run',
    ),
    'kofam_dir': NextflowParameter(
        type=typing.Optional[str],
        default='./kofam/',
        section_title=None,
        description="Path to a directory with KOfam files. Will be created if it doesn't exist.",
    ),
    'hmmdir': NextflowParameter(
        type=typing.Optional[LatchDir],
        default=None,
        section_title=None,
        description='Directory with hmm files which will be searched for among ORFs',
    ),
    'hmmfiles': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Comma-separated list of hmm files which will be searched for among ORFs',
    ),
    'hmmpattern': NextflowParameter(
        type=typing.Optional[str],
        default='*.hmm',
        section_title=None,
        description='specify which pattern hmm files end with',
    ),
    'skip_eukulele': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title='Taxonomy annotation options',
        description='skip eukulele run',
    ),
    'eukulele_method': NextflowParameter(
        type=typing.Optional[str],
        default='mets',
        section_title=None,
        description='Specify which method to use for EUKulele. the alternatives are: mets (metatranscriptomics) or  mags (Metagenome Assembled Genomes). default: mets',
    ),
    'eukulele_db': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='EUKulele database.',
    ),
    'eukulele_dbpath': NextflowParameter(
        type=typing.Optional[str],
        default='./eukulele/',
        section_title=None,
        description='EUKulele database folder.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

